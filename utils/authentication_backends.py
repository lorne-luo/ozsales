from django.contrib.auth.models import User
from apps.member.models import Seller


class MyCustomBackend:
    def authenticate(self, username=None, password=None):
        try:
            user = Seller.objects.get(username=username)
        except Seller.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                try:
                    django_user = User.objects.get(username=user.username)
                except User.DoesNotExist:
                    django_user = User(username=user.username, password=user.password)
                    django_user.is_staff = True
                    django_user.save()
                return django_user
            else:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class UsernameBackend:
    def authenticate(self, username=None):
        try:
            user = Seller.objects.get(username=username)
            return user
        except Seller.DoesNotExist:
            return None
