from django.contrib import admin
from attachments.models import Attachment
from authentication.models import CustomUser
from dialogue.models import Dialogue
from friend.models import Friend
from message.models import Message

# Регистрируем модели в админке
admin.site.register(Attachment)
admin.site.register(CustomUser)
admin.site.register(Dialogue)
admin.site.register(Friend)
admin.site.register(Message)
