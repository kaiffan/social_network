from attachments.models import Attachment
from authentication import serializers


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachment_url', 'attachment_type', 'message_id']
