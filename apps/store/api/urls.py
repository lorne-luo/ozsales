from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:store-list'), reverse('api:store-detail', kwargs={'pk': 1})
router.register(r'store', views.StoreViewSet, base_name='store')
router.register(r'page', views.PageViewSet, base_name='page')

urlpatterns = [

]

urlpatterns += router.urls
