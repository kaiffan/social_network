from django.db import models
from authentication.models import CustomUser


class Friend(models.Model):
    status_list = [
        ("ACCEPTED", "accepted"),
        ("WAITING", "waiting"),
    ]

    friendship_date = models.DateTimeField(name="friendship_date", auto_now_add=True, null=False)
    status = models.CharField(name="status", choices=status_list, default="WAITING", null=False)
    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        name="user",
        related_name='sent_friend_requests'
    )
    friend_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        name="friend",
        related_name='received_friend_requests'
    )

    class Meta:
        db_table = 'friend'
        unique_together = ('user_id', 'friend_id')
