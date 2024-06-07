from django.db import models
from authentication.models import CustomUser


class Dialogue(models.Model):
    title = models.CharField(name="title", null=False)
    avatar = models.CharField(name="avatar", max_length=255, null=False, default="")
    is_chat = models.BooleanField(name="is_chat", null=False, default=True)
    is_pinned = models.BooleanField(name="is_pinned", null=False, default=False)

    class Meta:
        db_table = 'dialogue'


class DialogueUser(models.Model):
    id_dialogue = models.ForeignKey(
        Dialogue,
        on_delete=models.CASCADE,
        name="dialogue"
    )
    id_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        name="user"
    )

    class Meta:
        db_table = 'dialogue_user'
