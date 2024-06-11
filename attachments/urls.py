from django.urls import path
from attachments.views import upload_file

urlpatterns = [
    path('attachments/upload_file', upload_file, name="upload_file"),
]