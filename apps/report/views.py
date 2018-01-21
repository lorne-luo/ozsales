# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin, SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.permission import ProfileRequiredMixin
from core.django.views import CommonContextMixin
from .models import MonthlyReport
from . import forms


class MonthlyReportListView(ProfileRequiredMixin, CommonContextMixin, ListView):
    """ List views for MonthlyReport """
    model = MonthlyReport
    template_name_suffix = '_list'  # report/monthlyreport_list.html
    profile_required = ['member.seller']


    def get_context_data(self, **kwargs):
        context = super(MonthlyReportListView, self).get_context_data(**kwargs)
        data = MonthlyReport.stat_user_total(self.request.user)
        context.update(data)
        return context


class MonthlyReportAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportAddForm
    template_name = 'adminlte/common_form.html'


class MonthlyReportUpdateView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportUpdateForm
    template_name = 'adminlte/common_form.html'


class MonthlyReportDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportDetailForm
    template_name = 'adminlte/common_detail_new.html'
