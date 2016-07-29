# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import Page, Store


class PageAddForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageDetailForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageUpdateForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']



class StoreAddForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreDetailForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreUpdateForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


