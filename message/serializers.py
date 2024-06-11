from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from message.models import Message
from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer


class MessageSerializer(ModelSerializer[Message]):
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'date_receive',
            'is_read',
            "user_sender_id",
            "user_recipient_id",
            'dialogue_id',
            'attachments'
        ]

    def get_attachments(self, message: Message):
        attachments = Attachment.objects.filter(message_id=message.id).all()
        return AttachmentSerializer(attachments, many=True).data


class UpdateMessageFieldSerializer(ModelSerializer[Message]):
    class Meta:
        model = Message
        fields = ['is_read', 'text']
