from django.urls import path
from dialogue.views import delete_dialog, add_dialogue


urlpatterns = [
    path('dialogue/<int:dialogue_id>/delete', delete_dialog, name="delete_dialog"),
    path('dialogue/add', add_dialogue, name="add_dialogue")
]