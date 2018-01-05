# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from core.django.views import CommonContextMixin
from . import forms
from models import Address, Customer


# views for Address

class AddressListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Address
    template_name_suffix = '_list'  # customer/address_list.html
    permissions = {
        "all": ("customer.view_address",)
    }


class AddressAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Address
    form_class = forms.AddressAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("address.add_address",)
    }


class AddressUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Address
    form_class = forms.AddressUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("address.change_address",)
    }


class AddressDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Address
    form_class = forms.AddressDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("address.view_address",)
    }


# views for Customer

class CustomerListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Customer
    template_name_suffix = '_list'  # customer/customer_list.html
    permissions = {
        "all": ("customer.view_customer",)
    }


class CustomerAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Customer
    form_class = forms.CustomerAddForm
    template_name = 'customer/customer_add.html'
    permissions = {
        "all": ("customer.add_customer",)
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.seller = self.request.profile
        return super(CustomerAddView, self).form_valid(form)


class CustomerUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Customer
    form_class = forms.CustomerUpdateForm
    template_name = 'customer/customer_edit.html'
    permissions = {
        "all": ("customer.change_customer",)
    }

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)

        context['new_address_forms'] = forms.AddressInlineForm(prefix='address_set')
        address_forms = forms.AddressFormSet(queryset=self.object.address_set.all(), prefix='address_set')
        context['address_forms'] = address_forms

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # customer address
        address_formset = forms.AddressFormSet(request.POST, request.FILES, prefix='address_set')
        for form in address_formset:
            form.is_valid()
            if form.instance.address or form.instance.name:
                form.fields['customer'].initial = self.object.id
                form.base_fields['customer'].initial = self.object.id
                form.changed_data.append('customer')
                form.instance.customer_id = self.object.id
            else:
                form._changed_data = []
            if form._errors and 'customer' in form._errors:
                del form._errors['customer']

        if not address_formset.is_valid():
            return HttpResponse(str(address_formset.errors))
        address_formset.save()

        return super(CustomerUpdateView, self).post(request, *args, **kwargs)


class CustomerDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Customer
    form_class = forms.CustomerDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("customer.view_customer",)
    }
