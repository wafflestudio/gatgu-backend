from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from user.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(allow_blank=False)
    #password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    #last_login = serializers.DateTimeField(read_only=True)
    userprofile = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    #area = serializers.CharField(write_only=True, allow_blank=False, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'userprofile',
            'created_at',
            'updated_at',
            'is_active',
        )

    def get_userprofile(self, user):
        return UserProfileSerializer(user.userprofile,
                                     context=self.context).data

    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if bool(first_name) ^ bool(last_name):
            api_exception = serializers.ValidationError("First name and last name should appear together.")
            api_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise api_exception
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            api_exception = serializers.ValidationError("First name or last name should not have number.")
            api_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise api_exception

        # profile_serializer = UserProfileSerializer(data=data, context=self.context)
        # profile_serializer.is_valid(raise_exception=True)

        return data

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('address', '')
        validated_data.pop('nickname', '')
        validated_data.pop('phonenumber', '')
        validated_data.pop('user_type', None)
        validated_data.pop('picture', None)
        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)

        return user

    def update(self, user, validated_data):
        address = validated_data.get('address')
        nickname = validated_data.get('nickname')
        phonenumber = validated_data.get('phonenumber')
        picture = validated_data.get('picture')

        # user_type = validated_data.pop('user_type', '')

        profile = user.userprofile
        if address is not None:
            profile.address = address
        if nickname is not None:
            profile.nickname = nickname
        if phonenumber is not None:
            profile.phonenumber = phonenumber
        if picture is not None:
            profile.picture = picture
        #        if user_type is not None:
        #            profile.user_type = user_type
        profile.save()

        return super(UserSerializer, self).update(user, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source='id')
    user_type = serializers.ChoiceField(write_only=True, allow_null=True, required=False, choices=UserProfile.USER_TYPE)
    nickname = serializers.CharField(write_only=True, allow_blank=False, required=False)
    phonenumber = serializers.CharField(write_only=True,
                                  allow_blank=False,
                                  max_length=13,
                                  required=False,
                                  validators=[RegexValidator(regex=r'^[0-9]{3}-([0-9]{3}|[0-9]{4})-[0-9]{4}$',
                                                             message="Phone number must be entered in the format '000-0000-0000'",
                                                             )
                                              ]
                                  )
    withdrew_at = serializers.DateTimeField(read_only=True,allow_null=True)
    picture = serializers.ImageField(write_only=True, required=False, allow_null=True, use_url=True)
    #profile_pics = serializers.ImageField(write_only=True, required=False, allow_null=True, use_url=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'profile_id',
            'user_type',
            'address',
            'nickname',
            'phonenumber',
            'picture',
        ]
