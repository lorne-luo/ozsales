
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
router.include_root_view = False

urlpatterns = patterns('apps.order.views',

)


router.register(r'api/express/expressorder', views.ExpressOrderViewSet, base_name='api-expressorder')


urlpatterns += router.urls