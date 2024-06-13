from rest_framework.serializers import ModelSerializer

from authentication.models import CustomUser


class UpdateUserFieldSerializer(ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'avatar',
            'theme'
        ]


class UserInfoSerializer(ModelSerializer[CustomUser]):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'registration_date',
            'avatar',
            'chat_background'
        ]

