from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager


class AuthUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @property
    def profile(self):
        if self.is_seller:
            return self.seller
        elif self.is_customer:
            return self.customer
        return None

    @property
    def is_seller(self):
        return getattr(self, 'seller') is not None

    @property
    def is_customer(self):
        return getattr(self, 'customer') is not None

    def __str__(self):
        return '%s' % self.get_username()
