# coding=utf-8
import stripe
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import ProcessFormView
from djstripe.enums import SubscriptionStatus
from djstripe.models import Card, Plan, Subscription
from djstripe.mixins import PaymentsContextMixin, SubscriptionMixin

from core.django.permission import SellerRequiredMixin


class UpdateCreditCardView(SellerRequiredMixin, PaymentsContextMixin, TemplateView):
    """A view to render the add card template."""
    template_name = "djstripe/add_card.html"

    def post(self, request, *args, **kwargs):
        token = request.POST.get("cardToken", None)

        if token is None:
            messages.error(self.request, 'Some errors happened, please retry.')
            raise Http404

        try:
            profile = self.request.profile
            card = profile.add_card(source=token, remove_old=True)  # input card token or detail dict
        except stripe.error.CardError as ex:
            context = self.get_context_data(**kwargs)
            context.update({'error': ex._message})
            return self.render_to_response(context)

        messages.success(self.request, 'Your credit card updated.')
        return HttpResponseRedirect(reverse_lazy('payments:view_card'))


class RemoveAllCardView(SellerRequiredMixin, RedirectView):
    http_method_names = ['post']
    pattern_name = 'payments:add_card'

    def post(self, request, *args, **kwargs):
        profile = self.request.profile
        profile.remove_all_card()
        profile.cancel_premium()
        return super(RemoveAllCardView, self).post(request, *args, **kwargs)


class RemoveSingleCardView(SellerRequiredMixin, RedirectView):
    http_method_names = ['post']
    pattern_name = 'payments:add_card'

    def post(self, request, *args, **kwargs):
        card_id = kwargs.get("pk")
        card = Card.objects.filter(pk=card_id).first()
        profile = self.request.profile
        if card:
            profile.remove_card(card.stripe_id)

        if not profile.get_all_card().count():
            profile.cancel_premium()

        return super(RemoveSingleCardView, self).post(request, *args, **kwargs)


class ViewCreditCardView(SellerRequiredMixin, PaymentsContextMixin, DetailView):
    template_name = "djstripe/view_card.html"

    def get_object(self, queryset=None):
        return self.request.profile.get_default_card()

    # uncomment if show subscription cancel
    # def get_context_data(self, **kwargs):
    #     context = super(ViewCreditCardView, self).get_context_data(**kwargs)
    #     customer = self.request.profile.stripe_customer
    #     context.update({'subscription': customer.valid_subscriptions.first()})
    #     return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return HttpResponseRedirect(reverse_lazy('payments:add_card'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RemoveCreditCardView(SellerRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = self.request.profile
        profile.remove_all_card()
        return reverse_lazy('payments:add_card')


class PlanPurchaseView(SellerRequiredMixin, SubscriptionMixin, TemplateResponseMixin, ContextMixin, ProcessFormView):
    template_name = 'djstripe/plan_purchase.html'

    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('selected_plan')
        plan = Plan.objects.filter(stripe_id=plan_id).first()
        if plan:
            customer = self.request.profile.stripe_customer
            subscription = customer.subscribe(plan)
            # todo update seller expiration, wrap subscribe method
        else:
            messages.success(self.request, 'Plan subcribe failed.')
            return HttpResponseRedirect(reverse_lazy('payments:plan_purchase'))
        return HttpResponseRedirect(reverse_lazy('payments:view_card'))


class CancelSubscriptionView(SellerRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        sub_stripe_id = kwargs.get("stripe_id")
        sub = Subscription.objects.filter(stripe_id=sub_stripe_id).first()

        if not sub:
            return reverse_lazy('payments:view_card')

        subscription = sub.cancel(at_period_end=True)
        if subscription.status == SubscriptionStatus.canceled:
            messages.info(self.request, '会员资格已取消.')
            return reverse_lazy('payments:view_card')
        elif subscription.cancel_at_period_end:
            # If pro-rate, they get some time to stay.
            messages.info(self.request, '会员资格将在%s到期后取消.' % subscription.current_period_end)
        return reverse_lazy('payments:view_card')
