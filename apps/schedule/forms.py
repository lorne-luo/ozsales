# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import DealSubscribe


class DealSubscribeAddForm(ModelForm):
    """ Add form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']


class DealSubscribeDetailForm(ModelForm):
    """ Detail form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']


class DealSubscribeUpdateForm(ModelForm):
    """ Update form for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']

