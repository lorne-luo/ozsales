from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import Product, Brand


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class BrandAddForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'country', 'remarks']


class BrandUpdateForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'country', 'remarks']


class BrandDetailForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'country', 'remarks']
