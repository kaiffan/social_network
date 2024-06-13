from django.urls import path
from friend.views import *

urlpatterns = [
    path('friends/<int:friend_id>/delete', delete_friend, name="delete_friend"),
    path('friends/<int:friend_id>/request', request_to_add_friend, name="request_to_add_friend"),
    path('friends/all', get_all_friends_user, name="get_all_friends_user"),
    path('friends/<int:friend_id>/add', add_friend, name="add_friend"),
    path('friends/incoming_request', get_incoming_requests, name="get_incoming_requests"),
    path('friends/outcoming_request', get_outcoming_requests, name="get_outcoming_requests"),
    path('friends/<int:friend_id>/reject_out', reject_request_outcoming_friend, name="reject_request_to_add_friend"),
    path('friends/<int:friend_id>/reject_inc', reject_request_incoming_friend, name="reject_request_incoming_friend")
]
