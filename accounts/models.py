from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    UserManager,
    AbstractUser,
    PermissionsMixin,
)
from django.utils import timezone


class CustomManager(BaseUserManager):
    def create_user(self, email, first_name, surname, password=None):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            surname=surname,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, surname, password=None):
        user = self.create_user(email, first_name, surname, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=254)
    surname = models.CharField(max_length=254)

    date_joined = models.DateTimeField(default=timezone.now)

    # Flags
    is_staff = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "surname"]

    def __str__(self):
        return self.email

    # Behaviours
    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active"])

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active"])
