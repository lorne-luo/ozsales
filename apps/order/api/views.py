"""
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
"""

import logging
import json

from apps.order.api import serializers
from ..models import Order
from utils.api.views import PaginateMaxModelViewSet, PaginateMaxListAPIView
from utils.api.permission import ModelPermissions

log = logging.getLogger(__name__)


class OrderViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing Channel instances.
     Holds custom single object views but not custom list views
    """
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.filter()
    order_by = ['create_time']

# class NormalChannelViewSet(ChannelViewSet):
#     queryset = Channel.objects.filter(is_hidden=False)

