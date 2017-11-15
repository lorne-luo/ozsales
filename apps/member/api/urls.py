from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from core.api.routers import PostHackedRouter
import views


urlpatterns = [
	url(r'^profile/$', views.Profile.as_view(), name='profile'),
	url(r'^api-token-auth/', obtain_auth_token, name='login-token'),
	url(r'^groups_and_users/$', views.GroupsAndUsersList.as_view(), name='groups-and-users'),
]

router = PostHackedRouter()
router.include_root_view = False
router.register(r'user', views.SellerViewSet, 'user')

urlpatterns += router.urls
