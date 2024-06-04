from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_date, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, birth_date, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
