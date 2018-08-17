# coding=utf-8
from core.django.forms import NoManytoManyHintModelForm
from .models import Page, Store


class PageAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']



class StoreAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


