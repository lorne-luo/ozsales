from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views


urlpatterns = []
router = DefaultRouter()
router.include_root_view = False

# urls for page
urlpatterns += patterns('',
    url(r'^store/page/add/$', login_required(views.PageAddView.as_view()), name="page-add"),
    url(r'^store/page/list/$', login_required(views.PageListView.as_view()), name='page-list'),
    url(r'^store/page/(?P<pk>\d+)/$', login_required(views.PageDetailView.as_view()), name="page-detail"),
    url(r'^store/page/(?P<pk>\d+)/edit/$', login_required(views.PageUpdateView.as_view()), name="page-update"),
    url(r'^store/page/delete/$', views.PageDeleteView.as_view(), name='page-delete'),
)

# reverse('api-page-list'),reverse('api-page-detail', kwargs={'pk': 1})
router.register(r'api/store/page', views.PageViewSet, base_name='api-page')


# urls for store
urlpatterns += patterns('',
    url(r'^store/store/add/$', login_required(views.StoreAddView.as_view()), name="store-add"),
    url(r'^store/store/list/$', login_required(views.StoreListView.as_view()), name='store-list'),
    url(r'^store/store/(?P<pk>\d+)/$', login_required(views.StoreDetailView.as_view()), name="store-detail"),
    url(r'^store/store/(?P<pk>\d+)/edit/$', login_required(views.StoreUpdateView.as_view()), name="store-update"),
    url(r'^store/store/delete/$', views.StoreDeleteView.as_view(), name='store-delete'),
)

# reverse('api-store-list'),reverse('api-store-detail', kwargs={'pk': 1})
router.register(r'api/store/store', views.StoreViewSet, base_name='api-store')


urlpatterns += router.urls