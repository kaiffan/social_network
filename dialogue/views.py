from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from dialogue.models import Dialogue, DialogueUser
from rest_framework import status
from dialogue.serializers import DialogueSerializer


@api_view(http_method_names=['GET'])
def get_all_dialogue_user(request: Request, user_id: int) -> Response:
    try:
        user_dialogues_rows = DialogueUser.objects.filter(user_id=user_id).all()
        user_dialogues = [row.dialogue_id for row in user_dialogues_rows]
    except DialogueUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        dialogues = Dialogue.objects.filter(id__in=user_dialogues).all()
        serializer = DialogueSerializer(dialogues, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


