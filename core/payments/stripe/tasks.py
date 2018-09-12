import logging
from celery import shared_task
from stripe.error import StripeError

log = logging.getLogger(__name__)


@shared_task(bind=True)
def process_webhook_event(self, event_id):
    """ Processes events from Stripe asynchronously. """
    from djstripe.models import Event
    event = Event.objects.filter(pk=event_id).first()
    if event:
        try:
            event.process(raise_exception=True)
            log.info("Stripe callback succeed: %s", str(event))
        except StripeError as exc:
            log.error("Failed to process Stripe event: %s", str(event))
            raise self.retry(exc=exc, countdown=30)  # retry after 60 seconds


def webhook_event_callback(event):
    """
         Dispatches the event to celery for processing.
         configure on https://dashboard.stripe.com/account/webhooks to make this webhook works.
    """
    # Ansychronous hand-off to celery so that we can continue immediately
    process_webhook_event(event.id)
