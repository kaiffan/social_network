from django.urls import path
from personal_account.views import update_user_info


urlpatterns = [
    path('personal_account/update', update_user_info, name="update_user_info")
]