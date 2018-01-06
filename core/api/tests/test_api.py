from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from utils.testbase import BaseWebTest
from apps.member.models import Seller


class APITest(BaseWebTest):
    fixtures = ['deploy/init_user.json']

    def setUp(self):
        self.admin_header = {'Authorization': "Token %s" % str(Seller.objects.get(username='admin').get_token())}
        super(APITest, self).setUp()
