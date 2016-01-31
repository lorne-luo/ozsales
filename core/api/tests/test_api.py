from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from utils.testbase import BaseWebTest
from apps.member.models import Seller


class APITest(BaseWebTest):
    fixtures = ['deploy/init_user.json']

    def setUp(self):
        self.admin_header = {'Authorization': "Token %s" % str(Seller.objects.get(username='admin').get_token())}
        super(APITest, self).setUp()

    def test_list_api(self):
        url = reverse('common_api:listcreate_api', kwargs={'app_name': 'member', 'model_name': 'seller'})
        result = self.app.get(url, headers=self.admin_header, status=200).json
        self.assertEqual(result['count'], 1)
        self.assertEqual(result['results'][0]['username'], 'admin')

    def test_create_api(self):
        user_count = Seller.objects.all().count()
        url = reverse('common_api:listcreate_api', kwargs={'app_name': 'member', 'model_name': 'seller'})
        data = {'username': 'admin2', 'password': '111111', 'password2': '111111', 'email': '1@1.com',
                'mobile': '1333333333', 'name':'admin2'}
        result = self.app.post(url, data, headers=self.admin_header, status=201).json
        self.assertEqual(result['name'], 'admin2')
        self.assertEqual(Seller.objects.all().count(), user_count + 1)

    def test_retrive_api(self):
        url = reverse('common_api:retriveupdate_api', kwargs={'app_name': 'member', 'model_name': 'seller', 'pk': 1})
        result = self.app.get(url, headers=self.admin_header, status=200).json
        self.assertEqual(result['username'], 'admin')

    def test_patch_api(self):
        url = reverse('common_api:retriveupdate_api', kwargs={'app_name': 'member', 'model_name': 'seller', 'pk': 1})
        data = {'name': 'admin3'}
        result = self.app.patch(url, data, headers=self.admin_header, status=200).json
        self.assertEqual(result['name'], 'admin3')

    def test_put_api(self):
        url = reverse('common_api:retriveupdate_api', kwargs={'app_name': 'member', 'model_name': 'seller', 'pk': 1})
        data = {'name': 'admin4'}
        result = self.app.put(url, data, headers=self.admin_header, status=200).json
        self.assertEqual(result['name'], 'admin4')