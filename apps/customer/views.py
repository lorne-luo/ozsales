from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from braces.views import MultiplePermissionsRequiredMixin

from models import Customer
from forms import CustomerForm

class CustomerList(MultiplePermissionsRequiredMixin, TemplateView):
    ''' List of objects. '''
    template_name = 'customer/customer-list.html'
    permissions = {
        "any": ("customer.add_customer", "customer.view_customer")
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('-last_order_time')
        return self.render_to_response(context)


class CustomerAddEdit(MultiplePermissionsRequiredMixin, TemplateView):
    ''' Add/Edit a object. '''
    template_name = 'customer/customer-edit.html'
    permissions = {
        "any": ("customer.add_customer", "customer.view_customer")
    }

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        context = {'form': CustomerForm(), }
        if pk:
            customer = get_object_or_404(Customer, id=pk)
            context['customer'] = customer

        return self.render_to_response(context)
