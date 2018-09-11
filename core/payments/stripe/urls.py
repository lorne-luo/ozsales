from django.conf.urls import url
from djstripe.views import WebHook
from . import views

urlpatterns = [
    url(r"^webhook/$", WebHook.as_view(), name="webhook"),
    url(r'^view_card/$', views.ViewCreditCardView.as_view(), name='view_card'),
    url(r'^add_card/$', views.UpdateCreditCardView.as_view(), name='add_card'),
    url(r'^remove_card/$', views.RemoveCreditCardView.as_view(), name='remove_card'),
    # url(r'^plan_purchase/$', views.PlanPurchaseView.as_view(), name='plan_purchase'),
    # url(r'^cancel_subscription/(?P<stripe_id>\w+)/$', views.CancelSubscriptionView.as_view(), name='cancel_subscription'),
    url(r'^remove_card/all/$', views.RemoveAllCardView.as_view(), name='remove_all_card'),
    url(r'^remove_card/(?P<pk>[-\w]+)/$', views.RemoveSingleCardView.as_view(), name='remove_card'),

    # url(r'^plan/confirm/(?P<plan_id>[-\w]+)/$', views.PlanPurchaseView.as_view(), name='plan_confirm'),
]
