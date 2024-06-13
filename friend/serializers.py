from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import CustomUser
from authentication.serializers import ShortCustomUserSerializer
from friend.models import Friend


class FriendSerializer(ModelSerializer[Friend]):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = [
            'friendship_date',
            'status',
            'friend_id',
            'user_sender_id',
            'user_info'
        ]
        extra_kwargs = {
            'friendship_date': {'required': False},
            'status': {'required': False},
            'user_sender_id': {'required': False},
            'friend_id': {'required': False},
            'user_info': {'required': False},
        }

    def get_user_info(self, friend):
        if friend.flag_reverse:
            friend_info = CustomUser.objects.get(id=friend.friend_id)
        else:
            friend_info = CustomUser.objects.get(id=friend.user_id)
        return ShortCustomUserSerializer(friend_info).data


class FriendShortSerializer(ModelSerializer[Friend]):
    class Meta:
        model = Friend
        fields = ['status', 'friend_id', 'user_sender_id', 'user_id']
        extra_kwargs = {
            'status': {'required': False},
            'friend_id': {'required': False},
            'user_sender_id': {'required': False},
            'user_id': {'required': False}
        }