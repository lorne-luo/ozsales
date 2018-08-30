from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:expresscarrier-list'), reverse('api:expresscarrier-detail', kwargs={'pk': 1})
router.register(r'carrier', views.ExpressCarrierViewSet, base_name='expresscarrier')
router.register(r'parcel', views.ExpressOrderViewSet, base_name='expressorder')

urlpatterns = [
    url(r'^carrier/autocomplete/$', views.ExpressCarrierAutocomplete.as_view(), name='carrier-autocomplete'),
]

urlpatterns += router.urls
