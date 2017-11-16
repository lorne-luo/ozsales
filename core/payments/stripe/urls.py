from django.conf.urls import url
import views

urlpatterns = [
    url(r'^payments/add_card/$', views.UpdateCreditCardView.as_view(), name='add_card'),
]
