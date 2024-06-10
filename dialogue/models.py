from django.db import models
from authentication.models import CustomUser


class Dialogue(models.Model):
    title = models.CharField(name="title", null=False)
    avatar = models.CharField(name="avatar", max_length=255, null=True, default="")
    is_pinned = models.BooleanField(name="is_pinned", null=False, default=False)

    class Meta:
        db_table = 'dialogue'


class DialogueUser(models.Model):
    dialogue = models.ForeignKey(
        Dialogue,
        on_delete=models.CASCADE,
        name="dialogue"
    )
    user_sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="sent_dialogue_users"
    )

    user_recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="received_dialogue_users"
    )

    class Meta:
        unique_together = ('user_sender', 'user_recipient')
        db_table = 'dialogue_user'
