from signal import raise_signal
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        if username is None:
            raise ValueError("Username is required!")
        if password is None:
            raise ValueError("Password is required!")
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        if username is None:
            raise ValueError("Username is required!")
        if password is None:
            raise ValueError("Password is required!")
        user = self.create_user(username, password)
        user.is_superuser, user.is_staff = True, True
        user.save()
        return user
