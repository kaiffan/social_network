from rest_framework.serializers import ModelSerializer
from message.models import Message


class MessageSerializer(ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'date_receive',
            'is_read',
            "user_sender_id",
            "user_recipient_id",
            'dialogue_id'
        ]


class UpdateMessageFieldSerializer(ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = ['is_read', 'text']