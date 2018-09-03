from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:expresscarrier-list'), reverse('api:expresscarrier-detail', kwargs={'pk': 1})
router.register(r'default_carrier', views.DefaultCarrierViewSet, base_name='default_carrier')

urlpatterns = [
    url(r'^default_carrier/autocomplete/$', views.DefaultCarrierAutocomplete.as_view(), name='default_carrier-autocomplete'),
]

urlpatterns += router.urls
