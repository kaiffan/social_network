from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import RegistrationView, LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('registrations/', RegistrationView.as_view(), name="registration_view"),
    path('login/', LoginView.as_view(), name="login_view"),
    path('logout/', LogoutView.as_view(), name="logout_view"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]