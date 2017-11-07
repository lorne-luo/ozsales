# -*- coding: utf-8 -*-
import logging
from django.core.context_processors import csrf
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
        return render_to_response('adminlte/login.html', RequestContext(request, c))
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


class Profile(PermissionRequiredMixin, TemplateView):
    template_name = 'member/profile.html'
    permission_required = 'member.view_seller'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        if pk:  # Admin editing other user's profile
            try:
                user = Seller.objects.get(pk=pk)
            except Seller.DoesNotExist:
                log.error("No user pk %s." % pk)
                raise Http404()
        else:  # Editing own profile
            user = request.user
        if request.user.has_perm('member.add_seller'):
            form = SellerProfileForm(username_readonly=False, instance=user)
        else:
            form = SellerProfileForm(username_readonly=True, instance=user)

        context = {
            'edit_user': user,
            'form': form,
            'resetpasswordform': _reset_password_form(user, request),
        }

        return self.render_to_response(context)


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
                return redirect('admin-user-edit', pk=user.pk)
    return render_to_response('member/user-reset-password.html', {
        'form': form,
        'edit_user': user
    }, RequestContext(request))


def _reset_password_form(user, request, POST=False):
    if user == request.user:
        form = UserResetPasswordForm(user)
        if POST:
            form = UserResetPasswordForm(user, POST)
    elif request.user.has_perm('member.change_seller'):
        form = ResetPasswordEmailForm(user)
        if POST:
            form = ResetPasswordEmailForm(user, POST)
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
    template_name = 'member/register.html'
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

        return super(RegisterView, self).form_valid(form)
