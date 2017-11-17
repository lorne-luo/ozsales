from django.conf.urls import url
from djstripe.views import WebHook
import views

urlpatterns = [
    url(r'^payments/add_card/$', views.UpdateCreditCardView.as_view(), name='add_card'),
    url(r"^payments/webhook/$", WebHook.as_view(), name="webhook"),
]
