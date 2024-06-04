from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("first_name", max_length=25, null=False)
    last_name = models.CharField("last_name", max_length=25, null=False)
    email = models.EmailField("email", max_length=255, unique=True, null=False)
    birth_date = models.DateField("birth_date", null=False)
    password = models.CharField("password", max_length=255, default="", null=False)
    date_registration = models.DateTimeField("date_registration", default=timezone.now(), null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'custom_user'