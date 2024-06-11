from rest_framework.serializers import ModelSerializer
from friend.models import Friend
from rest_framework import serializers
from authentication.models import CustomUser
from authentication.serializers import ShortCustomUserSerializer


class FriendSerializer(ModelSerializer[Friend]):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = [
            'friendship_date',
            'status',
            'friend_id',
            'user_info'
        ]
        extra_kwargs = {
            'friendship_date': {'required': False},
            'status': {'required': False},
            'friend_id': {'required': False},
            'user_info': {'required': False},
        }

    def get_user_info(self, friend):
        friend_info = CustomUser.objects.get(id=friend.friend_id)
        return ShortCustomUserSerializer(friend_info).data


class FriendUpdateFieldSerializer(ModelSerializer[Friend]):
    class Meta:
        model = Friend
        fields = ['status']