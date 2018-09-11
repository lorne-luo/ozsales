from django.conf.urls import url
from . import views

# urls for CarrierTracker
urlpatterns = [
    url(r'^carriertracker/add/$', views.CarrierTrackerAddView.as_view(), name='carriertracker-add'),
    url(r'^carriertracker/list/$', views.CarrierTrackerListView.as_view(), name='carriertracker-list'),
    url(r'^carriertracker/(?P<pk>[-\w]+)/$', views.CarrierTrackerDetailView.as_view(), name='carriertracker-detail'),
    url(r'^carriertracker/(?P<pk>[-\w]+)/edit/$', views.CarrierTrackerUpdateView.as_view(), name='carriertracker-update'),
]

