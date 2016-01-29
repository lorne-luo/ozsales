from django import forms
from models import Page, Store


class PageAddForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageUpdateForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class PageDetailForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'url', 'store', 'price', 'original_price']


class StoreAddForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreUpdateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreDetailForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']

