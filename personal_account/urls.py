from personal_account.views import update_user_info, upload_image
from django.urls import path


urlpatterns = [
    path('personal_account/update', update_user_info, name="update_user_info"),
    path('personal_account/upload_image', upload_image, name="upload_photo")
]