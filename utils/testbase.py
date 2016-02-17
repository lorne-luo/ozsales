from django_webtest import WebTest
from django.core import management
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase, TestCase
from django.contrib.auth.models import Group
from django.test.client import Client
# from rest_framework.test import APIClient
from apps.member.models import Seller


class BaseWebTest(WebTest):
    def setUp(self):
        super(BaseWebTest, self).setUp()

        self.client = Client()

        login_success = self.client.login(username='admin', password='admin')
        self.assertTrue(login_success)

        # self.api_client = APIClient()
        # login_success = self.api_client.login(username='admin', password='admin')
        # self.assertTrue(login_success)

        # login = self.app.post(reverse('api:login'), {'username': 'admin', 'password': 'admin'}, status=200)
        # login = login.json
        # self.admin = Seller.objects.get(username="admin")
        # self.assertFalse(self.admin.is_admin())
        # self.admin_header = {'Authorization': "Token %s" % str(login['token'])}
