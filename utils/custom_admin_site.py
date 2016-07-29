#coding=utf-8
from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.admin.sites import AdminSite


class CustomAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy(u'OZ商品管理系统')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy(u'OZ商品管理系统')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy(u'OZ商品管理系统')

    login_form = None
    index_template = None
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse('%s:logout' % self.name, current_app=self.name):
                    index_path = reverse('%s:index' % self.name, current_app=self.name)
                    return HttpResponseRedirect(index_path)
                # Inner import to prevent django.contrib.admin (app) from
                # importing django.contrib.auth.models.User (unrelated model).
                from django.contrib.auth.views import redirect_to_login

                return redirect_to_login(
                    request.get_full_path(),
                    reverse('%s:login' % self.name, current_app=self.name)
                )
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_urls(self):
        from django.conf.urls import patterns, url, include
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = patterns('',
                               url(r'^%s/main$' % self.name, wrap(self.index), name='index'),
                               url(r'^%s/login/$' % self.name, self.login, name='login'),
                               url(r'^%s/logout/$' % self.name, wrap(self.logout), name='logout'),
                               url(r'^%s/password_change/$' % self.name, wrap(self.password_change, cacheable=True),
                                   name='password_change'),
                               url(r'^password_change/done/$', wrap(self.password_change_done, cacheable=True),
                                   name='password_change_done'),
                               url(r'^%s/jsi18n/$' % self.name, wrap(self.i18n_javascript, cacheable=True),
                                   name='jsi18n'),
                               url(r'^%s/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$' % self.name,
                                   wrap(contenttype_views.shortcut), name='view_on_site'),
        )

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += patterns('',
                                    url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name),
                                        include(model_admin.urls))
            )
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += patterns('',
                                    url(regex, wrap(self.app_index), name='app_list'),
            )
        return urlpatterns

    def password_change(self, request):
        """
        Handles the "change password" task -- both form display and validation.
        """
        from django.contrib.auth.views import password_change

        url = reverse('%s:password_change_done' % self.name, current_app=self.name)
        defaults = {
            'current_app': self.name,
            'post_change_redirect': url,
            'extra_context': self.each_context(),
        }
        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template
        return password_change(request, **defaults)

    @never_cache
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse('%s:index' % self.name, current_app=self.name)
            return HttpResponseRedirect(index_path)

        from django.contrib.auth.views import login
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.admin.forms eventually imports User.
        from django.contrib.admin.forms import AdminAuthenticationForm

        context = dict(self.each_context(),
                       title=_('Log in'),
                       app_path=request.get_full_path(),
        )
        if (REDIRECT_FIELD_NAME not in request.GET and
                    REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = request.get_full_path()
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return login(request, **defaults)

    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_dict = {}
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)

            if has_module_perms:
                perms = model_admin.get_model_perms(request)

                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse(
                                '%s:%s_%s_changelist' % (self.name, app_label, model._meta.model_name),
                                current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse(
                                '%s:%s_%s_add' % (self.name, app_label, model._meta.model_name), current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': apps.get_app_config(app_label).verbose_name,
                            'app_label': app_label,
                            'app_url': reverse('%s:app_list' % self.name, kwargs={'app_label': app_label},
                                               current_app=self.name),
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }

        # Sort the apps alphabetically.
        app_list = list(six.itervalues(app_dict))
        app_list.sort(key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        context = dict(
            self.each_context(),
            title=self.index_title,
            app_list=app_list,
        )
        context.update(extra_context or {})
        return TemplateResponse(request, self.index_template or
                                         'admin/index.html', context,
                                current_app=self.name)

    def app_index(self, request, app_label, extra_context=None):
        user = request.user
        app_name = apps.get_app_config(app_label).verbose_name
        has_module_perms = user.has_module_perms(app_label)
        if not has_module_perms:
            raise PermissionDenied
        app_dict = {}
        for model, model_admin in self._registry.items():
            if app_label == model._meta.app_label:
                perms = model_admin.get_model_perms(request)

                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change'):
                        try:
                            model_dict['admin_url'] = reverse(
                                '%s:%s_%s_changelist' % (self.name, app_label, model._meta.model_name),
                                current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add'):
                        try:
                            model_dict['add_url'] = reverse(
                                '%s:%s_%s_add' % (self.name, app_label, model._meta.model_name), current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if app_dict:
                        app_dict['models'].append(model_dict),
                    else:
                        # First time around, now that we know there's
                        # something to display, add in the necessary meta
                        # information.
                        app_dict = {
                            'name': app_name,
                            'app_label': app_label,
                            'app_url': '',
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        context = dict(self.each_context(),
                       title=_('%(app)s administration') % {'app': app_name},
                       app_list=[app_dict],
                       app_label=app_label,
        )
        context.update(extra_context or {})

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context, current_app=self.name)


member_site = CustomAdminSite(name='member')