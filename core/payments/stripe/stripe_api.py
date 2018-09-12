
import stripe as base_stripe
from django.conf import settings
from django.db import transaction

STRIPE_LIVE_MODE = getattr(settings, "STRIPE_LIVE_MODE", False)

if hasattr(settings, "STRIPE_PUBLIC_KEY"):
    STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
elif STRIPE_LIVE_MODE:
    STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_LIVE_PUBLIC_KEY", "")
else:
    STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_TEST_PUBLIC_KEY", "")

if STRIPE_LIVE_MODE:
    STRIPE_SECRET_KEY = getattr(settings, "STRIPE_LIVE_SECRET_KEY", "")
else:
    STRIPE_SECRET_KEY = getattr(settings, "STRIPE_TEST_SECRET_KEY", "")

base_stripe.api_key = STRIPE_SECRET_KEY

stripe = base_stripe


# def sync_subscriber(subscriber):
#     """Sync a Customer with Stripe api data."""
#     customer, _created = StCustomer.get_or_create(subscriber=subscriber)
#     customer = StCustomer.objects.get(pk=customer.pk)
#     try:
#         customer.sync_from_stripe_data(customer.api_retrieve())
#         customer._sync_subscriptions()
#         customer._sync_invoices()
#         customer._sync_cards()
#         customer._sync_charges()
#     except InvalidRequestError as e:
#         print("ERROR: " + str(e))
#     return customer

def forgive_invoice(invoice):
    stripe_invoice = invoice.api_retrieve()
    stripe_invoice.closed = True
    invoice.closed = True
    with transaction.atomic():
        stripe_invoice.save()
        invoice.sync_from_stripe_data(stripe_invoice)
