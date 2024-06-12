from personal_account.views import update_user_info, change_avatar_user
from django.urls import path


urlpatterns = [
    path('personal_account/update_info', update_user_info, name="update_user_info"),
    path('personal_account/change_avatar', change_avatar_user, name="change_avatar_user")
]