# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.views import password_change

from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.views.views import CommonPageViewMixin


class OwnerViewSetMixin(object):
    def get_queryset(self):
        qs = super(OwnerViewSetMixin, self).get_queryset()
        if self.request.user.is_seller:
            return qs.filter(seller=self.request.profile)
        elif self.request.user.is_customer:
            return qs.filter(customer=self.request.profile)
        else:
            return qs.none()


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('order:order-list-short'))
    else:
        return HttpResponseRedirect(reverse_lazy('member:member-login'))


class ChangePasswordView(CommonPageViewMixin, TemplateView):
    def post(self, request, **kwargs):
        self.request = request
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        context['page_title'] = u'修改密码'
        template_response = password_change(
            self.request,
            template_name='adminlte/change-password.html',
            extra_context=context
        )
        return template_response


class ChangePasswordDoneView(CommonPageViewMixin, TemplateView):
    template_name = 'adminlte/change-password-done.html'
