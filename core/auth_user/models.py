from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager


class AuthUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @property
    def profile(self):
        if getattr(self, 'seller'):
            return self.seller
        return None

    def __str__(self):
        return '%s' % self.get_username()
