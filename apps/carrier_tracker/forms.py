# coding=utf-8
from django import forms
from core.django.forms import NoManytoManyHintModelForm
from .models import CarrierTracker


class CarrierTrackerAddForm(NoManytoManyHintModelForm):
    website = forms.URLField(label='官网地址', max_length=30, required=True, help_text='官方网站地址')  # make mandatory

    class Meta:
        model = CarrierTracker
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'list_tag', 'list_id', 'list_class',
                  'item_tag', 'item_index']


class CarrierTrackerDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = CarrierTracker
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'need_id']


class CarrierTrackerUpdateForm(CarrierTrackerAddForm):
    pass


class CarrierTrackerAdminForm(CarrierTrackerUpdateForm):
    class Meta:
        model = CarrierTracker
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'need_id', 'list_tag', 'list_id', 'list_class', 'item_tag', 'item_index']
