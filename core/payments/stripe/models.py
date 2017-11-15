from decimal import Decimal

from django.core.exceptions import SuspiciousOperation
from djstripe.models import Customer, Charge
from djstripe.sync import sync_subscriber


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


# class StCharge(Charge, StBaseObject):
#     INVOICE_NUMBER_KEY = 'invoice_number'
#
#     class Meta:
#         proxy = True
#
#     def _attach_objects_hook(self, cls, data):
#         super(StCharge, self)._attach_objects_hook(cls, data)
#         invoice = Invoice.objects.filter(stripe_id=data['invoice']).first()
#         if invoice:
#             self.invoice = invoice
#
#
# class ChargeLog(models.Model):
#     """just to get unique id for invoice number"""
#
#     def get_invoice_number(self):
#         if not self.id:
#             self.save()
#         number = hex(self.id).split('x')[-1].upper()
#         return number.zfill(6)


class UserProfileStripeMixin(object):
    """mixin for stripe customer subscriber model"""

    def sync_stripe(self):
        """sync all payment data (customer,card,charge,invoice) from stripe"""
        sync_subscriber(self.auth_user)

    @property
    def stripe_customer(self):
        if not getattr(self, 'auth_user'):
            raise SuspiciousOperation('%s do not related with Stripe customer.' % self)
        customer, _created = Customer.get_or_create(subscriber=self.auth_user)
        return Customer.objects.get(pk=customer.id)

    def can_charge(self):
        return self.stripe_customer.can_charge()

    def charge(self, amount, currency="aud", **kwargs):
        """refer djstripe.stripe_objects.charge"""
        amount = Decimal(amount).quantize(Decimal('0.01'))
        charge = self.stripe_customer.charge(amount, currency, **kwargs)
        return charge

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

    def add_card(self, source, set_default=True):
        return self.stripe_customer.add_card(source, set_default=set_default)

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

    def get_all_charges(self):
        return Charge.objects.filter(customer_id=self.stripe_customer)
