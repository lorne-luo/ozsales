from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import Product, Brand


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductAddForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'pic', 'brand', 'spec1', 'spec2', 'spec3', 'normal_price', 'bargain_price',
                  'safe_sell_price', 'tb_url', 'wd_url', 'wx_url']

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all().order_by('name_en')


class ProductDetailForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'pic', 'brand', 'spec1', 'spec2', 'spec3', 'normal_price', 'bargain_price',
                  'safe_sell_price', 'tb_url', 'wd_url', 'wx_url']


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
