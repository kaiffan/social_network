from django.urls import path
from search.views import search_users_by_email, search_messages_in_dialogue

urlpatterns = [
    path('search/<str:keywoard>/<int:id_dialogue>', search_messages_in_dialogue, name='search_messages_in_dialogue'),
    path('search/<str:keyword>', search_users_by_email, name='search_friends_user'),
]
