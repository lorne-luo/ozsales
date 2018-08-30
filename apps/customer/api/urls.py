from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:customer-list'), reverse('api:customer-detail', kwargs={'pk': 1})
router.register(r'customer', views.CustomerViewSet, base_name='customer')
router.register(r'address', views.AddressViewSet, base_name='address')

urlpatterns = [
    url(r'^customer/autocomplete/$', views.CustomerAutocomplete.as_view(), name='customer-autocomplete'),
    url(r'^address/autocomplete/$', views.AddressAutocomplete.as_view(), name='address-autocomplete'),
]

urlpatterns += router.urls
