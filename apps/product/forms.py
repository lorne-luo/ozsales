from core.django.forms import NoManytoManyHintModelForm
from models import Product, Brand


class ProductAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'alias', 'pic', 'brand']

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all().order_by('name_en')


class ProductAdminForm(ProductAddForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'alias', 'pic', 'brand', 'brand_en', 'brand_cn', 'seller']


class ProductDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Product
        fields = ['name_en', 'name_cn', 'alias', 'pic', 'brand_en', 'brand_cn', 'last_sell_price', 'avg_sell_price',
                  'avg_cost']


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
