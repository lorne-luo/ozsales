# coding=utf-8
from django import forms
from core.django.forms import NoManytoManyHintModelForm
from .models import ExpressCarrier


class ExpressCarrierAddForm(NoManytoManyHintModelForm):
    website = forms.URLField(label='官网地址', max_length=30, required=True, help_text='官方网站地址')  # make mandatory

    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url']


class ExpressCarrierDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'is_default']


class ExpressCarrierUpdateForm(ExpressCarrierAddForm):
    pass


class ExpressCarrierAdminForm(ExpressCarrierUpdateForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'is_default']

