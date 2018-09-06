from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:expresscarrier-list'), reverse('api:expresscarrier-detail', kwargs={'pk': 1})
router.register(r'carrier_tracker', views.CarrierTrackerViewSet, base_name='carrier_tracker')

urlpatterns = [
    url(r'^carrier_tracker/autocomplete/$', views.CarrierTrackerAutocomplete.as_view(), name='carrier_tracker-autocomplete'),
]

urlpatterns += router.urls
