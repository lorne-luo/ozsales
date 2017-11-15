from core.payments.stripe.stripe_api import STRIPE_PUBLIC_KEY


class PaymentsContextMixin(object):
    """Adds checkout context to a view."""

    def get_context_data(self, **kwargs):
        """Inject STRIPE_PUBLIC_KEY and plans into context_data."""
        context = super(PaymentsContextMixin, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY,
        })

        return context
