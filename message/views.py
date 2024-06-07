from message.serializers import UpdateMessageFieldSerializer, MessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from message.models import Message
from django.db.models import OuterRef, Subquery
from dialogue.models import DialogueUser
from rest_framework import status


@api_view(http_method_names=['DELETE'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def delete_message(request: Request, message_id: int) -> Response:
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['PATCH'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def update_message(request: Request, message_id: int) -> Response:
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateMessageFieldSerializer(instance=message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_all_messages_in_dialogue(request: Request, dialogue_id: int) -> Response:
    try:
        messages = Message.objects.filter(dialogue_id=dialogue_id).all()
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MessageSerializer(messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_last_messages_in_dialogue(request: Request) -> Response:
    try:
        user_dialogues_rows = DialogueUser.objects.filter(user_id=request.user.id).all()
        user_dialogues = [row.dialogue_id for row in user_dialogues_rows]
    except DialogueUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        latest_messages_subquery = Message.objects.filter(
            dialogue=OuterRef('dialogue_id')
        ).order_by('date_receive').reverse().values('date_receive')[:1]
        messages = Message.objects.filter(
            dialogue_id__in=user_dialogues,
            date_receive=Subquery(latest_messages_subquery)
        ).select_related('dialogue')
        return Response(
            data=messages.values(
                'text',
                'date_receive',
                'dialogue__title',
                'dialogue__is_pinned',
                'is_read',
                'dialogue_id'
            ), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)