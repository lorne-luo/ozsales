from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from braces.views import MultiplePermissionsRequiredMixin

from core.adminlte.views import CommonListPageView, CommonCreatePageView, CommonDetailPageView, CommonUpdatePageView, \
    CommonDeletePageView
from models import Customer
from forms import CustomerEditForm, CustomerAddForm2


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
        context = {'form': CustomerAddForm2(), }
        if pk:
            customer = get_object_or_404(Customer, id=pk)
            context['customer'] = customer

        return self.render_to_response(context)


class CustomerListView(CommonListPageView):
    model = Customer


class CustomerCreateView(CommonCreatePageView):
    model = Customer

    def get(self, request, *args, **kwargs):
        self.object = None
        self.set_form_page_attributes(*args, **kwargs)
        form = CustomerAddForm2()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CustomerDetailView(CommonDetailPageView):
    model = Customer


class CustomerUpdateView(CommonUpdatePageView):
    model = Customer

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomerEditForm(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CustomerDeleteView(CommonDeletePageView):
    model = Customer