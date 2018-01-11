import logging
from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.exceptions import SuspiciousOperation
from stripe.error import (CardError, StripeError, APIConnectionError, AuthenticationError, InvalidRequestError,
                          RateLimitError)
from djstripe.models import Customer, Charge
from djstripe.sync import sync_subscriber

log = logging.getLogger(__name__)


class StripePaymentUserMixin(object):
    """mixin for stripe customer subscriber model"""

    @property
    def subscriber(self):
        # return django auth user
        return self.auth_user

    @property
    def stripe_customer(self):
        if (isinstance(self.subscriber, get_user_model())):
            customer, _created = Customer.get_or_create(subscriber=self.subscriber)
            return customer
        raise SuspiciousOperation('%s is not a valid subscriber' % self.subscriber)

    def sync_stripe(self):
        """sync all payment data (customer,card,charge,invoice) from stripe"""
        sync_subscriber(self.subscriber)

    def can_charge(self):
        return self.stripe_customer.can_charge()

    def charge(self, amount, currency="aud", **kwargs):
        """refer djstripe.stripe_objects.charge"""
        amount = Decimal(amount).quantize(Decimal('0.01'))

        try:
            charge = self.stripe_customer.charge(amount, currency, **kwargs)
            return charge.paid, charge
        except CardError as e:
            # charge declined
            body = e.json_body
            err = body.get('error', {})
            msg = 'status=%s, type=%s, code=%s, param=%s, msg=%s' % (e.http_status, err.get('type'), err.get('code'),
                                                                     err.get('param'), err.get('message'))
            log.error('[Payment CardError] %s' % msg)
            return False, err.get('message')
        except (RateLimitError, APIConnectionError) as e:
            # Too many requests made to the API too quickly / Network communication with Stripe failed
            log.error('[Payment Unavailable] %s' % e)
            return False, 'Payment gateway have temporal problem, please re-try later.'
        except (InvalidRequestError, AuthenticationError) as e:
            # Invalid parameters were supplied to Stripe's API / Authentication with Stripe's API failed (maybe you changed API keys recently)
            log.error('[Payment AuthError] %s' % e)
            return False, 'Payment gateway have critical problem, please contact administrator.'
        except StripeError as e:
            # Display a very generic error to the user, and maybe send yourself an email
            log.error('[Payment StripeError] %s' % e)
            return False, str(e)
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            log.error('[Payment OtherError] %s' % e)
            raise e

    def update_unique_card(self, source):
        """add new default card and remove other"""
        card = self.add_card(source)
        # only keep one card, remove all existed when update new
        for source in self.stripe_customer.sources.exclude(stripe_id=card.stripe_id):
            try:
                source.remove()
            except Exception as ex:
                continue
        return card

    def add_card(self, source, remove_old=False, set_default=True):
        set_default = remove_old or set_default
        card = self.stripe_customer.add_card(source, set_default=set_default)
        if remove_old:
            for source in self.stripe_customer.sources.exclude(stripe_id=card.stripe_id):
                try:
                    source.remove()
                except Exception as ex:
                    continue
        return card

    def remove_all_card(self):
        """remove credit card"""
        for source in self.stripe_customer.sources.all():
            try:
                source.remove()
            except Exception as ex:
                continue

    def remove_card(self, stripe_id):
        self.stripe_customer.sources.filter(stripe_id=stripe_id).first().remove()

    def get_default_card(self):
        """all credit card"""
        return self.stripe_customer.default_source

    def get_all_card(self):
        return self.stripe_customer.sources.all()

    def get_all_charges(self):
        return Charge.objects.filter(customer_id=self.stripe_customer)

    def remove_all_subscriptions(self):
        subscriptions = self.stripe_customer.valid_subscriptions
        for sub in subscriptions:
            sub.cancel(at_period_end=True)


class StripeInvoice(models.Model):
    """ invoice for stripe charge """
    charge = models.ForeignKey(Charge, blank=True, null=True)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    status = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    @property
    def number(self):
        if not self.id:
            self.save()
        number = hex(self.id).split('x')[-1].upper()
        return number.zfill(6)

    def update_from_charge(self, charge):
        self.charge = charge
        self.paid = charge.paid
        self.refunded = charge.refunded
        self.amount_refunded = charge.amount_refunded
        self.status = charge.status
        self.amount = charge.amount
        if self.amount_refunded and self.amount_refunded < self.refunded:
            self.status = 'PARTIALLY REFUNDED'

    @staticmethod
    def get_by_charge(charge):
        return StripeInvoice.objects.filter(charge=charge).first() or StripeInvoice()


@receiver(post_save, sender=Charge)
def update_invoice(sender, instance=None, created=False, update_fields=None, **kwargs):
    invoice = StripeInvoice.get_by_charge(instance)
    invoice.update_from_charge(instance)
    invoice.save()
