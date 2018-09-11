from django.core.management.base import BaseCommand

from djstripe.models import Plan


class Command(BaseCommand):
    help = "Sync plans from stripe to the local database"

    def handle(self, *args, **options):
        existed_ids = []
        for plan in Plan.api_list():
            stripe_id = plan.get('pk')
            if Plan.objects.filter(stripe_id=stripe_id).exists():
                print(('Plan id=%s updated.' % stripe_id))
            else:
                print(('Plan id=%s created.' % stripe_id))
            existed_ids.append(stripe_id)
            Plan.sync_from_stripe_data(plan)

        # for plan in Plan.objects.exclude(stripe_id__in=existed_ids):
        #     print('Plan id=%s deleted.' % plan.stripe_id)
        #     plan.delete()
