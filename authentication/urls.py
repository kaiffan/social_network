from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from authentication.views import registration_user, login_user, logout_user, get_user_id
from django.urls import path

urlpatterns = [
    path('registrations', registration_user, name="registration_view"),
    path('login', login_user, name="login_view"),
    path('logout', logout_user, name="logout_view"),
    path('user/id', get_user_id, name="get_user_id"),
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify', TokenVerifyView.as_view(), name="verify_token"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh")
]
