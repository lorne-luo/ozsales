from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:dealsubscribe-list'), reverse('api:dealsubscribe-detail', kwargs={'pk': 1})
router.register(r'dealsubscribe', views.DealSubscribeViewSet, base_name='dealsubscribe')

urlpatterns = [

]

urlpatterns += router.urls
