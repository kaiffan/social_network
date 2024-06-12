from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.core.files.storage import default_storage

from personal_account.serializers import UpdateUserFieldSerializer
from attachments.views import save_file_in_localhost
from authentication.models import CustomUser
from dotenv import load_dotenv

import os

load_dotenv()


@api_view(http_method_names=['PATCH'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def update_user_info(request: Request) -> Response:
    try:
        user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateUserFieldSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def change_avatar_user(request: Request) -> Response:
    user: CustomUser = CustomUser.objects.get(id=request.user.id)
    uploaded_file = request.FILES.get('image')
    if uploaded_file.name != '':
        name, extension = uploaded_file.name.split(".")
        if not (extension == 'jpg' or extension == 'jpeg'):
            return Response(data={"message": "Unsupported extension file"}, status=status.HTTP_400_BAD_REQUEST)
        filename = os.path.join(
            os.getenv('UPLOAD_DIRECTORY'),
            name[:-2] + "_" + str(request.user.id) + "." + extension
        )
        if os.path.exists(filename):
            os.remove(filename)
        save_file_in_localhost(filename=filename, uploaded_file=uploaded_file)
        user.avatar = "http://127.0.0.1:3000" + default_storage.url(filename)
        user.save()
        return Response(data={"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
