from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(allow_blank=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    userprofile = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(default=True)
    nickname = serializers.CharField(
        write_only=True,
        allow_blank=False,
        max_length=20,
        required=False,
    )
    picture = serializers.ImageField(
        write_only=True,
        allow_null=True,
        use_url=True,
        required=False,
    )
    participated_count = serializers.SerializerMethodField()
    hosted_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'userprofile',
            'is_active',
            'nickname',
            'picture',

            'participated_count',
            'hosted_count',

        )

    # def get_participated_count(self, user):
    #     part_cnt = user.participant_profile.count()
    #     hst_cnt = user.article.count()
    #
    #     return {"participanted_count":part_cnt,"hosted_count": hst_cnt}

    def get_participated_count(self, user):
        part_cnt = user.participant_profile.count()
        return part_cnt

    def get_hosted_count(self, user):
        hst_cnt = user.article.count()
        return hst_cnt

    def get_userprofile(self, user):
        try:
            return UserProfileSerializer(user.userprofile,
                                         context=self.context).data
        except ObjectDoesNotExist:

            message = "Cannot find your profile."
            api_exception = serializers.ValidationError(message)
            api_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise api_exception

    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if bool(first_name) ^ bool(last_name):
            message = "First name and last name should appear together."
            api_exception = serializers.ValidationError(message)
            api_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise api_exception
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            message = "First name or last name should not have number."
            api_exception = serializers.ValidationError(message)
            api_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise api_exception

        return data

    @transaction.atomic
    def create(self, validated_data):
        nickname = validated_data.pop('nickname', '')
        picture = validated_data.pop('picture', None)

        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)

        UserProfile.objects.create(user_id=user.id,
                                   nickname=nickname,
                                   picture=picture)

        return user

    def update(self, user, validated_data):

        nickname = validated_data.get('nickname')
        picture = validated_data.get('picture')

        profile = user.userprofile

        if nickname:
            profile.nickname = nickname
        if picture:
            profile.picture = picture

        profile.save()

        return super(UserSerializer, self).update(user, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        allow_blank=False,
        max_length=20
    )
    picture = serializers.ImageField(
        allow_null=True,
        use_url=True,
        required=False,
    )
    updated_at = serializers.DateTimeField(read_only=True)
    withdrew_at = serializers.DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'nickname',
            'picture',
            'updated_at',
            'withdrew_at',
            'picture',
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    participated_count = serializers.SerializerMethodField()
    hosted_count = serializers.SerializerMethodField()



    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'picture',
            'participated_count',
            'hosted_count',
        )

    def get_nickname(self, user):
        return user.userprofile.nickname

    def get_picture(self, user):
        return user.userprofile.picture


    def get_participated_count(self, user):
        part_cnt = user.participant_profile.count()
        return part_cnt

    def get_hosted_count(self, user):
        hst_cnt = user.article.count()
        return hst_cnt
#
class TokenResponseSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()

    def get_token(self,user):
        refresh = TokenObtainPairSerializer.get_token(user)
        data = dict()
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

