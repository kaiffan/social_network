from django.db import models

from message.models import Message


class Attachment(models.Model):
    type_attachment = [
        ("FILE", "file"),
        ("IMAGE", "image"),
        ("VIDEO", "video")
    ]

    attachment_url = models.CharField(name="attachment_url", null=True, max_length=255)
    attachment_type = models.TextField(name="attachment_type", null=False, choices=type_attachment)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, name="message")

    class Meta:
        db_table = 'attachment'
