from core.django.forms import NoManytoManyHintModelForm
from models import Product, Brand


class ProductForm(NoManytoManyHintModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'pic', 'brand', 'spec', 'tb_url', 'wd_url', 'wx_url']

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all().order_by('name_en')


class ProductDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'pic', 'brand_en', 'brand_cn', 'spec',
                  'last_sell_price', 'avg_sell_price', 'avg_cost', 'tb_url', 'wd_url', 'wx_url']


class BrandAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'short_name', 'remarks']


class BrandUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'short_name', 'remarks']


class BrandDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_cn', 'short_name', 'remarks']
