from rest_framework.serializers import ModelSerializer
from friend.models import Friend


class FriendSerializer(ModelSerializer[Friend]):
    class Meta:
        model = Friend
        fields = [
            'friendship_date',
            'status',
            'user_id',
            'friend_id'
        ]
        extra_kwargs = {
            'friendship_date': {'required': False},
            'status': {'required': False},
            'user_id': {'required': False},
            'friend_id': {'required': False},
        }


class FriendUpdateFieldSerializer(ModelSerializer[Friend]):
    class Meta:
        model = Friend
        fields = ['status']


class FriendAddSerializer(ModelSerializer[Friend]):
    class Meta:
        model = Friend
        fields = [
            'friend_id'
        ]