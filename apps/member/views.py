# -*- coding: utf-8 -*-
import logging
from django.template.context_processors import csrf
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from braces.views import PermissionRequiredMixin
from smtplib import SMTPException, SMTPConnectError
import socket

from .models import Seller
from .forms import SellerProfileForm, UserResetPasswordForm, ResetPasswordEmailForm, RegisterForm, LoginForm

log = logging.getLogger(__name__)


@sensitive_post_parameters()
@csrf_exempt
@ensure_csrf_cookie
@never_cache
def member_login(request):
    if request.method == 'GET':
        c = csrf(request)
        if request.GET.get('next'):
            c.update({'next': request.GET['next']})
        c.update({'form': LoginForm()})
        return render_to_response('adminlte/login.html', c)
    elif request.method == 'POST':
        old_user = request.user or None
        form = LoginForm(request.POST)
        if not form.is_valid():
            form.data = {'mobile': form.data.get('mobile')}
            return render_to_response('adminlte/login.html', {'form': form})

        mobile = form.cleaned_data.get('mobile')
        password = form.cleaned_data.get('password')
        user = authenticate(username=mobile, password=password)
        if user:
            login(request, user)
            next_page = request.POST.get('next', None)
            # If the user was already logged-in before we ignore the ?next
            # parameter, this avoids a loop of login prompts when the user does
            # not have the permission to see the page in ?next
            if old_user == user or not next_page:
                # Redirect chefs to meals page
                next_page = reverse('order:order-list-short')

            return HttpResponseRedirect(next_page)
        else:
            form.add_error(None, u'密码错误，请重试')
            form.data = {'mobile': mobile}
            return render_to_response('adminlte/login.html', {'form': form})


def member_home(request):
    return HttpResponse('123')


def member_logout(request):
    logout(request)
    return redirect('member-login')


class CreateUser(PermissionRequiredMixin, TemplateView):
    template_name = 'member/profile.html'
    permission_required = 'member.add_seller'

    def get(self, request, *args, **kwargs):
        context = {'form': SellerProfileForm(username_readonly=False)}
        return self.render_to_response(context)


class ProfileView(PermissionRequiredMixin, FormView):
    form_class = SellerProfileForm
    template_name = 'member/profile.html'
    permission_required = 'member.change_seller'
    success_url = reverse_lazy('member-profile')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', '')
        if pk and self.request.user.is_superuser:  # Admin editing other user's profile
            try:
                return Seller.objects.get(auth_user_id=pk)
            except Seller.DoesNotExist:
                raise Http404()
        elif self.request.user.is_seller:  # Editing own profile
            return self.request.user.profile
        else:
            raise Http404()

    def get_initial(self):
        return {'email': self.request.user.email, 'mobile': self.request.user.mobile}

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        self.object = self.get_object()
        kwargs.update({'instance': self.object})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({'object': self.object})
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.mobile = form.cleaned_data.get('mobile')

        password = form.cleaned_data.get('password')
        if password:
            self.request.user.set_password(password)
        self.request.user.save()
        messages.success(self.request, u'个人资料已更新')
        return super(ProfileView, self).form_valid(form)


@permission_required('member.add_seller', raise_exception=True)
def seller_index(request):
    if request.user.is_superuser:
        users = Seller.objects.all().exclude(username=request.user.username)
    elif request.user.is_group('Admin'):
        users = Seller.objects.exclude(is_superuser=True).exclude(username=request.user.username)
    else:
        users = Seller.objects.exclude(groups__name='Admin').exclude(is_superuser=True).exclude(
            username=request.user.username)

    return render_to_response('member/user-list.html', {'users': users},
                              RequestContext(request))


def user_password_reset(request, pk):
    user = get_object_or_404(Seller, pk=pk)
    allowed_change_other = (request.user.groups.filter(name='Admin').exists() or
                            request.user.is_superuser or
                            request.user.has_perm('member.add_seller'))
    if not request.user == user and not allowed_change_other:
        log.error('Response forbidden, lacking permission to change other users.')
        return HttpResponseForbidden()

    form = _reset_password_form(user, request)
    if request.method == "POST":
        form = _reset_password_form(user, request, request.POST)

        if form.is_valid():
            try:
                form.save()
            except SMTPException, (value, message):
                messages.error(request, 'SMTP error while sending user notification: Error %s (%s)' % (value, message))
            except (SMTPConnectError, socket.error), (value, message):
                messages.error(request, 'Error while connecting to SMTP server: Error %s (%s)' % (value, message))

            # user.renew_token()
            if request.user == user:
                return redirect('member-profile')
            else:
                return redirect('admin-seller-edit', pk=user.pk)
    return render_to_response('member/user-reset-password.html', {
        'form': form,
        'edit_user': user
    }, RequestContext(request))


def _reset_password_form(seller, request, POST=False):
    if seller == request.user.profile:
        form = UserResetPasswordForm(seller)
        if POST:
            form = UserResetPasswordForm(seller, POST)
    elif request.user.is_superuser:
        form = ResetPasswordEmailForm(seller)
        if POST:
            form = ResetPasswordEmailForm(seller, POST)
    else:
        log.error('Lacking permission to change user.')
        raise Http404

    return form


@permission_required('member.delete_seller', raise_exception=True)
def user_delete(request, pk):
    try:
        Seller.objects.get(pk=pk).delete()
    except Seller.DoesNotExist:
        pass
    return redirect('seller-index')


class AgentView(TemplateView):
    template_name = 'member/agent.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RegisterView(FormView):
    template_name = 'adminlte/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('member-login')

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        mobile = form.cleaned_data.get('mobile')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        Seller.create_seller(mobile, email, password)
        messages.success(self.request, '注册成功, 请登陆.')

        return super(RegisterView, self).form_valid(form)
