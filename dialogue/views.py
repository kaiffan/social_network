from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from dialogue.serializers import DialogueSerializer
from dialogue.models import Dialogue, DialogueUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import CustomUser


@api_view(http_method_names=['DELETE'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def delete_dialog(request: Request, dialogue_id: int) -> Response:
    try:
        dialogue = Dialogue.objects.get(id=dialogue_id)
    except Dialogue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        dialogue.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def add_dialogue(request: Request, user_recipient_id: int) -> Response:
    dialogue_data = request.data.copy()
    user_recipient_data = CustomUser.objects.get(id=user_recipient_id)
    dialogue_data['title'] = user_recipient_data.first_name + ' ' + user_recipient_data.last_name
    dialogue_data['avatar'] = user_recipient_data.avatar

    dialogue_serializer = DialogueSerializer(data=dialogue_data)

    if request.method == 'POST':
        dialogue_serializer.is_valid(raise_exception=True)
        dialogue = dialogue_serializer.save()
        try:
            dialogue_user_sender = DialogueUser(
                dialogue_id=dialogue.id,
                user_sender_id=request.user.id,
                user_recipient_id=user_recipient_id
            )
            dialogue_user_recipient = DialogueUser(
                dialogue_id=dialogue.id,
                user_sender_id=user_recipient_id,
                user_recipient_id=request.user.id
            )
            DialogueUser.objects.bulk_create([dialogue_user_sender, dialogue_user_recipient])
        except IntegrityError:
            return Response(data={"error": "This dialogue user already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=dialogue.id, status=status.HTTP_201_CREATED)
    return Response(dialogue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
