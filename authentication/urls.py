from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import registration_user, login_user, logout_user
from django.urls import path

urlpatterns = [
    path('registrations/', registration_user, name="registration_view"),
    path('login/', login_user, name="login_view"),
    path('logout/', logout_user, name="logout_view"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]