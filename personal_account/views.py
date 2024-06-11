from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.core.files.storage import default_storage

from personal_account.serializers import UpdateUserFieldSerializer
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
def upload_image(request: Request) -> Response:
    uploaded_file = request.FILES.get('image')
    if uploaded_file.name != '':
        name, extension = uploaded_file.name.split(".")
        print(name)
        filename = os.path.join(
            os.getenv('UPLOAD_DIRECTORY'),
            name[:-2] + "_" + str(request.user.id) + "." + extension
        )
        print(filename)
        if os.path.exists(filename):
            os.remove(filename)
        default_storage.save(filename, ContentFile(uploaded_file.read()))
        return Response(data={"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
