from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:brand-list'), reverse('api:brand-detail', kwargs={'pk': 1})
router.register(r'brand', views.BrandViewSet, base_name='brand')
router.register(r'product', views.ProductViewSet, base_name='product')

urlpatterns = [
    url(r'^product/product/autocomplete/$', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
]

urlpatterns += router.urls
