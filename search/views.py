from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from message.serializers import MessageSerializer
from message.models import Message

from search.serializers import SearchCustomUserSerializer
from authentication.models import CustomUser

from django.core.cache import cache

from rapidfuzz import process


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def search_users_by_email(request: Request, keyword: str) -> Response:
    cache_key: str = f'friends_' + keyword
    user_cache = cache.get(cache_key)
    if not user_cache:
        user_cache = CustomUser.objects.exclude(id=request.user.id).all()
        matches = process.extract(keyword, [user.email for user in user_cache], limit=5)
        top_users_emails = [match[0] for match in matches if match[1] > 50]
        user_cache = CustomUser.objects.filter(email__in=top_users_emails)
        if len(user_cache) == 0:
            user_cache = CustomUser.objects.exclude(id=request.user.id).all()
            serializer: SearchCustomUserSerializer = SearchCustomUserSerializer(user_cache, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        cache.set(cache_key, user_cache, timeout=150)
    serializer: SearchCustomUserSerializer = SearchCustomUserSerializer(user_cache, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def search_messages_in_dialogue(request: Request, keyword: str, id_dialogue: int) -> Response:
    cache_key: str = f'messages_' + keyword
    messages_in_dialogue = cache.get(cache_key)
    if not messages_in_dialogue:
        messages_in_dialogue = Message.objects.filter(id_dialogue=id_dialogue).all()
        matches = process.extract(keyword, [message.text for message in messages_in_dialogue], limit=15)
        top_text_messages = [match[0] for match in matches if match[1] > 70]
        messages_in_dialogue = Message.objects.filter(id_dialogue=id_dialogue).filter(text__in=top_text_messages)
        cache.set(cache_key, messages_in_dialogue, timeout=75)
    serializer: MessageSerializer = MessageSerializer(messages_in_dialogue, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
