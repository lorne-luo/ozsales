from django.conf.urls import url
from . import views

# urls for defaultcarrier
urlpatterns = [
    url(r'^defaultcarrier/add/$', views.DefaultCarrierAddView.as_view(), name='defaultcarrier-add'),
    url(r'^defaultcarrier/list/$', views.DefaultCarrierListView.as_view(), name='defaultcarrier-list'),
    url(r'^defaultcarrier/(?P<pk>\d+)/$', views.DefaultCarrierDetailView.as_view(), name='defaultcarrier-detail'),
    url(r'^defaultcarrier/(?P<pk>\d+)/edit/$', views.DefaultCarrierUpdateView.as_view(), name='defaultcarrier-update'),
]

