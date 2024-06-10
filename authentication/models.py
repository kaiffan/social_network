from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(name="first_name", max_length=25, null=False)
    last_name = models.CharField(name="last_name", max_length=25, null=False)
    email = models.EmailField(name="email", max_length=255, unique=True, null=False)
    birth_date = models.DateField(name="birth_date", null=False)
    password = models.CharField(name="password", max_length=255, default="", null=False)
    registration_date = models.DateTimeField(name="registration_date", auto_now_add=True, null=False)
    avatar = models.CharField(
        name="avatar",
        max_length=255,
        null=False,
        default="http://localhost:3000/static/images/default_avatar_user.jpg"
    )
    theme = models.BooleanField(name="theme", max_length=255, null=False, default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'custom_user'

    @property
    def tokens(self) -> dict[str, str]:
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
