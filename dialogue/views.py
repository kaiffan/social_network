from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from dialogue.serializers import DialogueSerializer
from dialogue.models import Dialogue, DialogueUser
from authentication.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
def add_dialogue(request: Request, user_id: int) -> Response:
    try:
        CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    dialogue_serializer = DialogueSerializer(data=request.data)

    if request.method == 'POST':
        dialogue_serializer.is_valid(raise_exception=True)
        dialogue = dialogue_serializer.save()
        dialogue_user = DialogueUser(dialogue_id=dialogue.id, user_id=user_id)
        DialogueUser.save(dialogue_user)
        return Response(status=status.HTTP_201_CREATED)
    return Response(dialogue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
