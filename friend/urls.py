from django.urls import path
from friend.views import delete_friend, update_status_friend, get_all_friends_user, add_friend


urlpatterns = [
    path('friends/<int:friend_id>/delete', delete_friend, name="delete_friend"),
    path('friends/<int:friend_id>/update', update_status_friend, name="update_status_friend"),
    path('friends/all', get_all_friends_user, name="get_all_friends_user"),
    path('friends/<int:friend_id>/add', add_friend, name="add_friend")
]