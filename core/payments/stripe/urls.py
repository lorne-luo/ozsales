from django.conf.urls import url
from djstripe.views import WebHook
import views

urlpatterns = [
    url(r"^payments/webhook/$", WebHook.as_view(), name="webhook"),
    url(r'^payments/view_card/$', views.ViewCreditCardView.as_view(), name='view_card'),
    url(r'^payments/add_card/$', views.UpdateCreditCardView.as_view(), name='add_card'),
    url(r'^payments/remove_card/$', views.RemoveCreditCardView.as_view(), name='remove_card'),
    url(r'^payments/plan_purchase/$', views.PlanPurchaseView.as_view(), name='plan_purchase'),
    url(r'^payments/remove_card/all/$', views.RemoveAllCardView.as_view(), name='remove_all_card'),
    url(r'^payments/remove_card/(?P<pk>\d+)/$', views.RemoveSingleCardView.as_view(), name='remove_card'),

    # url(r'^payments/plan/confirm/(?P<plan_id>\d+)/$', views.PlanPurchaseView.as_view(), name='plan_confirm'),
]
