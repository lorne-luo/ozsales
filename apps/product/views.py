from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from braces.views import MultiplePermissionsRequiredMixin

from models import Product
from forms import ProductForm

class ProductList(MultiplePermissionsRequiredMixin, TemplateView):
    ''' List of products. '''
    template_name = 'product/product-list.html'
    permissions = {
        "any": ("product.add_product", "product.view_product")
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return self.render_to_response(context)


class ProductAddEdit(MultiplePermissionsRequiredMixin, TemplateView):
    ''' Add/Edit a product. '''
    template_name = 'product/product-edit.html'
    permissions = {
        "any": ("product.add_product", "product.view_product")
    }

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        context = {'form': ProductForm(), }
        if pk:
            product = get_object_or_404(Product, id=pk)
            context['product'] = product

        return self.render_to_response(context)
