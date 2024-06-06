from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, ValidationError, Serializer
from authentication.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class RegistrationSerializer(ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'password',
                  'registration_date']

    def create(self, validated_data):
        return CustomUser.objects.create_user(first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              email=validated_data['email'],
                                              password=validated_data['password'],
                                              birth_date=validated_data['birth_date'])


class LoginSerializer(Serializer[CustomUser]):
    email = CharField(max_length=255)
    password = CharField(max_length=128, write_only=True)

    tokens = SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj.email)
        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']

    def validate(self, data):  # type: ignore
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
