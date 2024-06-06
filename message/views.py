from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from message.models import Message
from message.serializers import UpdateReadFieldSerializer, MessageSerializer


@api_view(http_method_names=['DELETE'])
def delete_message(request: Request, message_id: int) -> Response:
    try:
        message = Message.objects.filter(id=message_id).first()
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['PATCH'])
def update_message(request: Request, message_id: int) -> Response:
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateReadFieldSerializer(instance=message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def get_all_messages_in_dialogue(request: Request, dialogue_id: int) -> Response:
    try:
        messages = Message.objects.filter(dialogue_id=dialogue_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MessageSerializer(messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
