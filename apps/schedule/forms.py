# coding=utf-8
from core.forms.forms import NoManytoManyHintModelForm
from models import DealSubscribe


class DealSubscribeAddForm(NoManytoManyHintModelForm):
    """ Add form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['mobile', 'includes', 'excludes', 'is_active']


class DealSubscribeDetailForm(NoManytoManyHintModelForm):
    """ Detail form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['mobile', 'includes', 'excludes', 'is_active', 'msg_count']


class DealSubscribeUpdateForm(NoManytoManyHintModelForm):
    """ Update form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['mobile', 'includes', 'excludes', 'is_active']
