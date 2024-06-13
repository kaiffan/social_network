import os

from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def upload_file(request: Request) -> Response:
    uploaded_file = request.FILES.get('file')
    if uploaded_file.name != '':
        filename = os.path.join(os.getenv('UPLOAD_FILES_DIRECTORY'), uploaded_file.name)
        save_file_in_localhost(filename=filename, uploaded_file=uploaded_file)
        file_url = "http://127.0.0.1:3000" + default_storage.url(filename)
        return Response(data={"message": "File uploaded successfully", "url": file_url},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(data={"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)


def save_file_in_localhost(filename, uploaded_file) -> None:
    with open(filename, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
