from django.urls import re_path
from dialogue.consumers import DialogueConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<dialogue_id>\w+)/$', DialogueConsumer.as_asgi()),
]
