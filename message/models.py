from django.db import models
from authentication.models import CustomUser
from dialogue.models import Dialogue


class Message(models.Model):
    text = models.TextField(name="text", null=False)
    date_receive = models.DateTimeField(name="date_receive", null=False, auto_now_add=True)
    is_read = models.BooleanField(name="is_read", null=False, default=False)
    id_user_sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        name="user_sender",
        related_name='message_sender'
    )
    id_user_recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        name="user_recipient",
        related_name='message_received'
    )
    id_dialogue = models.ForeignKey(
        Dialogue,
        on_delete=models.CASCADE,
        name="dialogue"
    )

    class Meta:
        db_table = 'message'
