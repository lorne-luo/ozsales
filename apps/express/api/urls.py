from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:expresscarrier-list'), reverse('api:expresscarrier-detail', kwargs={'pk': 1})
router.register(r'expressorder', views.ExpressOrderViewSet, base_name='expressorder')
router.register(r'expresscarrier', views.ExpressCarrierViewSet, base_name='expresscarrier')

urlpatterns = [

]

urlpatterns += router.urls
