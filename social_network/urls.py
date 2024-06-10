from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('personal_account.urls')),
    path('', include('message.urls')),
    path('', include('dialogue.urls')),
    path('', include('friend.urls')),
    path('', include('search.urls')),
]
