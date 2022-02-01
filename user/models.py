from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, null=False, unique=True, db_index=True)
    username = models.CharField(
        max_length=255, unique=True, null=False,  db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
