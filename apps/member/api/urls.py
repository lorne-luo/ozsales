from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from core.api.routers import PostHackedRouter
from . import views

urlpatterns = [
    url(r'^register/verification_code/$', views.SendVerificationCode.as_view(), name='send_verification_code'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^api-token-auth/', obtain_auth_token, name='login-token'),
]

router = PostHackedRouter()
router.include_root_view = False
router.register(r'seller', views.SellerViewSet, base_name='seller')

urlpatterns += router.urls
