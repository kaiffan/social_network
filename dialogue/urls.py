from django.urls import path
from dialogue.views import get_all_dialogue_user


urlpatterns = [
    path('dialogue/<int:user_id>/all', get_all_dialogue_user, name="get_all_dialogue_user"),
]