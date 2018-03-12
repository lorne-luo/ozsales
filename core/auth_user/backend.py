from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


# AUTHENTICATION_BACKENDS

class AuthUserAuthenticateBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get('username') or kwargs.get('mobile') or kwargs.get('email')
        try:
            key = 'username'
            if username.isdigit():
                key = 'mobile'
            elif '@' in username:
                key = 'email'

            user = UserModel._default_manager.get(**{key: username})
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
