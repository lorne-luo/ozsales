# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import DealSubscribe


class DealTaskAddForm(ModelForm):
    """ Add form for DealTask """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']


class DealTaskDetailForm(ModelForm):
    """ Detail form for DealTask """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']


class DealTaskUpdateForm(ModelForm):
    """ Update form for DealTask """

    class Meta:
        model = DealSubscribe
        fields = ['includes', 'excludes', 'is_active']

