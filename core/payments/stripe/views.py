import stripe
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import ProcessFormView
from djstripe.models import Card, Plan
from djstripe.mixins import PaymentsContextMixin, SubscriptionMixin


class UpdateCreditCardView(LoginRequiredMixin, PaymentsContextMixin, TemplateView):
    """A view to render the add card template."""
    template_name = "djstripe/add_card.html"

    def post(self, request, *args, **kwargs):
        token = request.POST.get("cardToken", None)

        if token is None:
            messages.error(self.request, 'Some errors happened, please retry.')
            raise Http404

        try:
            profile = self.request.user.profile
            card = profile.add_card(source=token, remove_old=True)  # input card token or detail dict
        except stripe.error.CardError as ex:
            context = self.get_context_data(**kwargs)
            context.update({'error': ex._message})
            return self.render_to_response(context)

        messages.success(self.request, 'Your credit card updated.')
        return HttpResponseRedirect(reverse_lazy('payments:view_card'))


class RemoveAllCardView(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    pattern_name = 'payments:add_card'

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile
        profile.remove_all_card()
        return super(RemoveAllCardView, self).post(request, *args, **kwargs)


class RemoveSingleCardView(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    pattern_name = 'payments:add_card'

    def post(self, request, *args, **kwargs):
        card_id = kwargs.get("pk")
        card = Card.objects.filter(id=card_id).first()
        if card:
            profile = self.request.user.profile
            profile.remove_card(card.stripe_id)
        return super(RemoveSingleCardView, self).post(request, *args, **kwargs)


class ViewCreditCardView(LoginRequiredMixin, PaymentsContextMixin, DetailView):
    template_name = "djstripe/view_card.html"

    def get_object(self, queryset=None):
        return self.request.user.profile.get_default_card

    def get(self, request, *args, **kwargs):
        return super(ViewCreditCardView, self).get(request, *args, **kwargs)


class PlanPurchaseView(LoginRequiredMixin, SubscriptionMixin, TemplateResponseMixin, ContextMixin, ProcessFormView):
    template_name = 'djstripe/plan_purchase.html'

    def get_context_data(self, **kwargs):
        # todo template not finished
        return super(PlanPurchaseView, self).get_context_data()

    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('selected_plan')
        plan = Plan.objects.filter(stripe_id=plan_id).first()
        if plan:
            customer = self.request.user.profile.stripe_customer
            subscription = customer.subscribe(plan)
        else:
            messages.success(self.request, 'Your credit card updated.')
            return HttpResponseRedirect(reverse_lazy('payments:plan_purchase'))
        return HttpResponseRedirect(reverse_lazy('payments:view_card'))
