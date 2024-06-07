from django.urls import path
from message.views import (delete_message, update_message,
    get_all_messages_in_dialogue, get_last_messages_in_dialogue)

urlpatterns = [
    path('messages/<int:message_id>/delete', delete_message, name="delete_message"),
    path('messages/<int:message_id>/update', update_message, name="update_message"),
    path('messages/<int:dialogue_id>/all', get_all_messages_in_dialogue, name="get_all_messages_in_dialogue"),
    path('messages/last', get_last_messages_in_dialogue, name="get_last_messages_in_dialogue"),
]
