import datetime
from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, BooleanField, CharField, SerializerMethodField, ValidationError, \
    Serializer
from authentication.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class RegistrationSerializer(ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value


class LoginSerializer(Serializer[CustomUser]):
    email = CharField(max_length=255)
    password = CharField(max_length=128, write_only=True)
    theme = BooleanField(source="get_theme", read_only=True)
    tokens = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens', 'theme']

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj.email)
        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise ValidationError('An email address is required to log in.')

        if password is None:
            raise ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise ValidationError('This user is not currently activated.')

        return user


class LogoutSerializer(Serializer[CustomUser]):
    refresh = CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except TokenError as e:
            raise AuthenticationFailed(e)


class ShortCustomUserSerializer(ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'chat_background']


class UpdatePasswordSerializer(Serializer[CustomUser]):
    password = CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['password']

    def validate_password(self, value):
        validate_password(value)
        return value
