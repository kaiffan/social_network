from rest_framework.serializers import ModelSerializer
from message.models import Message


class MessageSerializer(ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = [
            'text',
            'avatar',
            'is_read',
            "user_sender_id",
            "user_recipient_id",
            'dialogue_id'
        ]


class UpdateReadFieldSerializer(ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = ['is_read', 'text', 'avatar']