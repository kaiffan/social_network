from personal_account.views import *
from django.urls import path


urlpatterns = [
    path('personal_account/update_info', update_user_info, name="update_user_info"),
    path('personal_account/change_avatar', change_avatar_user, name="change_avatar_user"),
    path('personal_account/user_info', get_user_info, name="get_user_info"),
    path('personal_account/update_password', update_password, name="update_password")
]