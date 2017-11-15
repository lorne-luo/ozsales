from decimal import Decimal

from django.db import models
from djstripe.models import Customer, Charge, Invoice
from djstripe.models import Card as StCard
from djstripe.stripe_objects import StripeCustomer


class StBaseObject(object):
    def sync(self):
        """sync single object from stripe according to stripe_id"""
        if self.stripe_id:
            data = self.stripe_class.retrieve(self.stripe_id)
            self._sync(self.__class__._stripe_object_to_record(data))
            self._attach_objects_hook(self.__class__, data)
            self.save()
            self._attach_objects_post_save_hook(self.__class__, data)

        return self


class StCustomer(Customer, StBaseObject):
    class Meta:
        proxy = True

    def _sync_cards(self, **kwargs):
        for stripe_card in StCard.api_list(customer=self, **kwargs):
            StCard.sync_from_stripe_data(stripe_card)

    def _sync_charges(self, **kwargs):
        for stripe_charge in Charge.api_list(customer=self.stripe_id, **kwargs):
            StCharge.sync_from_stripe_data(stripe_charge)

    def charge(self, amount, currency="aud", **kwargs):
        if not isinstance(amount, Decimal):
            amount = Decimal(amount).quantize(Decimal('0.01'))

        stripe_charge = StripeCustomer.charge(self, amount=amount, currency=currency, **kwargs)
        charge = StCharge.sync_from_stripe_data(stripe_charge)
        return charge


class StCharge(Charge, StBaseObject):
    INVOICE_NUMBER_KEY = 'invoice_number'

    class Meta:
        proxy = True

    def _attach_objects_hook(self, cls, data):
        super(StCharge, self)._attach_objects_hook(cls, data)
        invoice = Invoice.objects.filter(stripe_id=data['invoice']).first()
        if invoice:
            self.invoice = invoice

    def refund(self, amount=None, reason=None):
        refunded_charge = super(StCharge, self).refund(amount, reason)
        return StCharge.sync_from_stripe_data(refunded_charge)

    def capture(self):
        captured_charge = super(StCharge, self).capture()
        return StCharge.sync_from_stripe_data(captured_charge)

    @property
    def invoice_number(self):
        return self.metadata.get(self.INVOICE_NUMBER_KEY, None)


class ChargeLog(models.Model):
    """just to get unique id for invoice number"""

    def get_invoice_number(self):
        if not self.id:
            self.save()
        number = hex(self.id).split('x')[-1].upper()
        return number.zfill(6)
