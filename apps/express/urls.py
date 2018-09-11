from django.conf.urls import url
from . import views

# urls for expresscarrier
urlpatterns = [
    url(r'^expresscarrier/add/$', views.ExpressCarrierAddView.as_view(), name='expresscarrier-add'),
    url(r'^expresscarrier/list/$', views.ExpressCarrierListView.as_view(), name='expresscarrier-list'),
    url(r'^expresscarrier/(?P<pk>[-\w]+)/$', views.ExpressCarrierDetailView.as_view(), name='expresscarrier-detail'),
    url(r'^expresscarrier/(?P<pk>[-\w]+)/edit/$', views.ExpressCarrierUpdateView.as_view(), name='expresscarrier-update'),
]

