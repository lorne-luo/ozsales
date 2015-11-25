'''
Copyright (c) 2013 O7 Technologies Pty Ltd trading as Omniscreen. All Rights Reserved.

O7 Technologies Pty Ltd trading as Omniscreen ("Omniscreen") retains copyright
on all text, source and binary code contained in this software and documentation.
Omniscreen grants Licensee a limited license to use this software,
provided that this copyright notice and license appear on all copies of the software.
The software source code is provided for reference, compilation and porting purposes only
and may not be copied, modified or distributed in any manner and by any means
without prior written permission from Omniscreen.

THIS SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS,"
WITHOUT ANY WARRANTY OF ANY KIND. ALL EXPRESS OR IMPLIED CONDITIONS,
REPRESENTATIONS AND WARRANTIES, INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT, ARE HEREBY EXCLUDED.
OMNISCREEN SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE
AS A RESULT OF USING OR MODIFYING THE SOFTWARE OR ITS DERIVATIVES.

IN NO EVENT WILL OMNISCREEN BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA,
OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES,
HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
ARISING OUT OF THE USE OF OR INABILITY TO USE SOFTWARE,
EVEN IF OMNISCREEN HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
import views


urlpatterns = patterns('',
	url(r'^profile/$', views.Profile.as_view(), name='profile'),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='login-token'),
	url(r'^groups_and_users/$', views.GroupsAndUsersList.as_view(), name='groups-and-users'),
)

router = DefaultRouter()
router.include_root_view = False
router.register(r'user', views.SellerViewSet, 'user')
# router.register(r'billingaccount', views.BillingAccountViewSet)

urlpatterns += router.urls
