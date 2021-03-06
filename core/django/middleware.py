from django.contrib.auth.middleware import AuthenticationMiddleware


class ProfileAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super(ProfileAuthenticationMiddleware, self).process_request(request)
        profile = getattr(request.user, 'profile', None)
        setattr(request, 'profile', profile)
        if profile:
            if request.user.is_seller:
                setattr(request, 'seller', profile)
            if request.user.is_customer:
                setattr(request, 'customer', profile)
