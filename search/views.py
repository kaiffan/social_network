from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from message.serializers import MessageSerializer
from message.models import Message

from authentication.serializers import ShortCustomUserSerializer
from authentication.models import CustomUser

from django.core.cache import cache


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def search_users_by_email(request: Request, keyword: str) -> Response:
    cache_key: str = f'friends_' + keyword
    users = cache.get(cache_key)
    if not users:
        users = list(CustomUser.objects.filter(email__icontains=keyword).all())
        cache.set(cache_key, users, timeout=300)
    serializer: ShortCustomUserSerializer = ShortCustomUserSerializer(users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def search_messages_in_dialogue(request: Request, keyword: str, id_dialogue: int) -> Response:
    cache_key: str = f'messages_' + keyword
    messages = cache.get(cache_key)
    if not messages:
        messages = list(Message.objects.filter(id_dialogue=id_dialogue).filter(content__contains=keyword).all())
        cache.set(cache_key, messages, timeout=1200)
    serializer: MessageSerializer = MessageSerializer(messages, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
