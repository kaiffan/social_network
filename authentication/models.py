from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("first_name", max_length=25, null=False)
    last_name = models.CharField("last_name", max_length=25, null=False)
    email = models.EmailField("email", max_length=255, unique=True, null=False)
    birth_date = models.DateField("birth_date", null=False)
    password = models.CharField("password", max_length=255, default="", null=False)
    registration_date = models.DateTimeField("registration_date", auto_now_add=True, null=False)
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