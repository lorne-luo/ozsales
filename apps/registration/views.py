from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from forms import RegistrationForm, LoginForm


LOGIN_URL = '/auth/login/'

LOGOUT_URL = '/auth/logout/'


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        try:
            return settings.LOGIN_REDIRECT_URL
        except:
            return "/accounts/profile/"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['page_system_name'] = settings.SITE_NAME
        return context


class LogoutView(View):

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(LOGIN_URL)


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegistrationForm

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(LOGIN_URL)
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
        )

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    template_name = 'auth/success.html'
