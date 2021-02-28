from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.serializers import UserSerializer, UserProfileSerializer
from .models import User, UserProfile
import requests


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated(),)

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(),)
        return self.permission_classes

    # POST /user/ 회원가입
    @transaction.atomic
    def create(self, request):

        data = request.data

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            response_data = {
                "error": "username, password, email are required."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        nickname = data.get('nickname')

        if not nickname:
            response_data = {
                "error": "nickname are required."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(nickname__iexact=nickname,
                                      withdrew_at__isnull=True).exists():  # only active user couldn't conflict.
            response_data = {
                "error": "A user with that Nickname already exists."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        userprofile_serializer = UserProfileSerializer(data=data)
        userprofile_serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
        except IntegrityError:
            response_data = {
                "error": "A user with that username already exists."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = serializer.data
        data['token'] = user.auth_token.key
        return Response(data, status=status.HTTP_201_CREATED)

    # PUT /user/login/  로그인
    @action(detail=False, methods=['PUT'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            data = self.get_serializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data)

        response_data = {"error": "Wrong username or wrong password"}
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['PUT'])  # 로그아웃
    def logout(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

    # Get /user/{user_id} # 유저 정보 가져오기(나 & 남)
    def retrieve(self, request, pk=None):

        if pk == 'me':
            user = request.user
        else:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                response_data = {"message": "There is no such user."}
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_superuser:

            if not user.is_active or user.is_superuser:
                response_data = {
                    "message": "Coudn't get this user's information."}
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            else:
                pass
        else:
            pass

        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    def list(self, request):

        if request.user.is_superuser:
            users = User.objects.all()
        else:
            users = User.objects.filter(is_active=True, is_superuser=False)

        return Response(self.get_serializer(users, many=True).data, status=status.HTTP_200_OK)

    # 회원탈퇴
    @action(detail=False, methods=['PUT'], url_path='withdrawal', url_name='withdrawal')
    def withdrawal(self, request):

        user = request.user

        if user.is_active:
            profile = user.userprofile
            profile.withdrew_at = timezone.now()
            profile.save()
            user.is_active = False
            user.save()
        else:
            response_data = {"message": "This user Already withdrew"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Successfully deactivated."}, status=status.HTTP_200_OK)

    @transaction.atomic
    # PUT /user/me/  # 유저 정보 수정 (나)
    def update(self, request, pk=None):

        if pk != 'me':
            response_data = {"error": "Can't update other Users information"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        data = request.data

        cnt = 0

        for key in ['nickname', 'picture', 'password']:
            if key in data:
                cnt = cnt+1

        if cnt != len(data):
            response_data = {"error": "Request has invalid key"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        nickname = data.get('nickname')

        if UserProfile.objects.filter(nickname__iexact=nickname,
                                      withdrew_at__isnull=True).exclude(user_id=user.id).exists():
            response_data = {
                "error": "A user with that Nickname already exists."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.update(user, serializer.validated_data)

        return Response(serializer.data)


    @action(detail=True, methods=['GET'], url_path='activity')
    def hosted_list(self, request, pk):
        user_tar = self.get_object().id
        hosted = Article.objects.all().filter(deleted_at=None, writer_id=user_tar)
        data = ArticleSerializer(hosted, many=True).data
        return Response(data, status=status.HTTP_200_OK)

