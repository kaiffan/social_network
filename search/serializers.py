from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from authentication.models import CustomUser
from friend.models import Friend
from friend.serializers import FriendShortSerializer


class SearchCustomUserSerializer(ModelSerializer[CustomUser]):
    friend_info = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'chat_background', 'friend_info', ]

    def get_friend_info(self, user):
        friend_info = Friend.objects.filter(user_id=user.id).first()
        return FriendShortSerializer(friend_info).data