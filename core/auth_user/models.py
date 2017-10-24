from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager


class AuthUser(AbstractUser):
    @property
    def profile(self):
        if getattr(self,'seller'):
            return self.seller
        return None
