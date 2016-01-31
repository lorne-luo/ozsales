# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.core.exceptions import ViewDoesNotExist, ObjectDoesNotExist
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView, TemplateView, DetailView
from rest_framework.generics import GenericAPIView
from rest_framework_extensions.mixins import PaginateByMaxMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route, list_route
from rest_framework import filters, permissions
from apps.adminlte import constants
# from apps.adminlte.models import Menu, SystemConfig, Permission
# from apps.messageset.models import Notification, Task
# from apps.organization.models import Staff


def get_system_config_value(key_name):
    try:
        return 'site name'
    except:
        return u'未找到 %s 系统配置项' % key_name


class CommonContextMixin(object):
    @property
    def app_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.app_label
        else:
            raise SuspiciousOperation('CommonView cant get model info.')

    @property
    def model_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.model_name
        else:
            raise SuspiciousOperation('CommonView cant get model info.')

    def get_context_data(self, **kwargs):
        context = super(CommonContextMixin, self).get_context_data(**kwargs)

        default_dashboard_title = constants.DEFAULT_DASHBOARD_TITLE

        if getattr(self, 'object', None):
            page_title = unicode(self.object)
        elif getattr(self, 'model', None):
            page_title = self.model._meta.verbose_name
        else:
            page_title = default_dashboard_title

        page_model_perms = {
            'add': self.request.user.has_perm('%s.add_%s' % (self.app_name, self.model_name)),
            'change': self.request.user.has_perm('%s.change_%s' % (self.app_name, self.model_name)),
            'delete': self.request.user.has_perm('%s.delete_%s' % (self.app_name, self.model_name)),
            'view': self.request.user.has_perm('%s.view_%s' % (self.app_name, self.model_name))
        }

        common_dict = {
            'default_dashboard_title': default_dashboard_title,
            'page_title': page_title,
            'page_model': getattr(self, 'model', ''),
            'page_app_name': self.app_name,
            'page_model_name': self.model_name,
            'page_model_verbose_name': getattr(self, 'model')._meta.verbose_name,
            'page_system_name': get_system_config_value('system_name'),
            'page_system_subhead': get_system_config_value('system_subhead'),
            'page_model_perms': page_model_perms
        }
        context.update(common_dict)
        return context


class CommonPageViewMixin(object):
    model = None

    @property
    def app_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.app_label
        else:
            raise ViewDoesNotExist

    @property
    def model_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.model_name
        else:
            raise ViewDoesNotExist('No model found.')

    def get_model(self):
        if 'app_name' not in self.kwargs or 'model_name' not in self.kwargs:
            raise SuspiciousOperation('CommonView cant get app_name and model_name.')

        if not getattr(self, 'model', None):
            app_name = self.kwargs.get('app_name').lower()
            model_name = self.kwargs.get('model_name').lower()
            try:
                model_content_type = ContentType.objects.get(app_label=app_name, model=model_name)
            except ObjectDoesNotExist:
                raise ViewDoesNotExist
            setattr(self, 'model', model_content_type.model_class())

    def get_context_data(self, **kwargs):
        context = super(CommonPageViewMixin, self).get_context_data(**kwargs)
        default_dashboard_title = constants.DEFAULT_DASHBOARD_TITLE
        if hasattr(self, 'model'):
            page_title = getattr(self, 'model')._meta.verbose_name
        else:
            page_title = default_dashboard_title

        common_dict = {
            'default_dashboard_title': default_dashboard_title,
            'page_title': page_title,
            'page_model': getattr(self, 'model', ''),
            'page_app_name': self.app_name,
            'page_model_name': self.model_name,
            'page_system_name': get_system_config_value('system_name'),
            'page_system_subhead': get_system_config_value('system_subhead')
        }
        context.update(common_dict)
        return context


class IndexView(CommonPageViewMixin, TemplateView):
    template_name = "adminlte/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # staff_count = Staff.objects.filter(status=Staff.IN_JOB).count()
        # context['staff_count'] = staff_count
        return context


class CommonListPageView(CommonPageViewMixin, ListView):
    template_name = 'adminlte/common_list.html'

    def get(self, request, *args, **kwargs):
        self.get_model()
        if hasattr(getattr(self, 'model').Config, 'list_template_name'):
            self.template_name = getattr(self, 'model').Config.list_template_name
        return super(CommonListPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CommonListPageView, self).get_context_data(**kwargs)
        titles, fields = self.get_table_titles()
        context['table_titles'] = titles
        context['table_fields'] = list(fields)
        return context

    def get_table_titles(self):
        show_fields = getattr(self, 'model').Config.list_display_fields
        meta_fields = getattr(self, 'model')._meta.fields
        meta_names = [mf.name for mf in meta_fields]
        titles = []
        for name in show_fields:
            if name in meta_names:
                for mf in meta_fields:
                    if mf.name == name:
                        titles.append(mf.verbose_name)
            else:
                if not hasattr(getattr(self, 'model', None), name):
                    raise ImproperlyConfigured('Cant found field %s in %s' % (name, self.model._meta.model_name))
                field_property = getattr(self.model, name)
                if hasattr(field_property, '__call__'):
                    titles.append(field_property.short_description)
                elif hasattr(field_property, 'field'):
                    titles.append(field_property.field.verbose_name)
                else:
                    titles.append(name)  # add this field in serializer
        return titles, show_fields


class CommonFormPageMixin(CommonPageViewMixin):
    template_name = 'adminlte/common_form.html'

    def set_form_page_attributes(self, *args, **kwargs):
        self.get_model()

        if not getattr(self, 'fields', None):
            self.fields = getattr(self, 'model').Config.list_form_fields

        self.success_url = reverse(
            'adminlte:common_list_page',
            kwargs={
                'app_name': self.app_name,
                'model_name': self.model_name
            }
        )
        if hasattr(getattr(self, 'model').Config, 'form_template_name'):
            self.template_name = getattr(getattr(self, 'model').Config,
                                         'form_template_name')


class CommonCreatePageView(CommonFormPageMixin, CreateView):
    def get(self, request, *args, **kwargs):
        self.object = None
        self.set_form_page_attributes(*args, **kwargs)
        return super(CommonCreatePageView, self).get(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CommonCreatePageView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.set_form_page_attributes(*args, **kwargs)
        return super(CommonCreatePageView, self).post(request, *args, **kwargs)


class CommonDetailPageView(CommonPageViewMixin, DetailView):
    template_name = 'adminlte/common_detail.html'

    def get(self, request, *args, **kwargs):
        self.get_model()
        if hasattr(getattr(self, 'model').Config, 'detail_template_name'):
            self.template_name = getattr(self, 'model').Config.list_template_name
        return super(CommonDetailPageView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(CommonDetailPageView, self).get_object(queryset)
        if hasattr(getattr(self, 'model').Config, 'get_object_hook'):
            getattr(self, 'model').Config.get_object_hook(self.request, obj)
        return obj


class CommonUpdatePageView(CommonFormPageMixin, UpdateView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.set_form_page_attributes(*self.args, **self.kwargs)
        return getattr(self, 'model').objects.filter(pk=pk)


class CommonDeletePageView(CommonFormPageMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        objects = self.get_object()
        for obj in objects:
            obj.delete()
        return JsonResponse({'result': True}, status=200)

    def get_queryset(self):
        self.set_form_page_attributes(*self.args, **self.kwargs)
        return getattr(self, 'model').objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get('pk')
        pk = pk.split(',')
        return queryset.filter(pk__in=pk)


# class CommonBatchDeleteView(GenericAPIView):
#     permission_classes = [permissions.DjangoModelPermissions]
#
#     def post(self, request):
#         pk = self.request.POST.get('pk')
#         pk = pk.split(',')
#         objects = self.queryset.filter(pk__in=pk)
#         for obj in objects:
#             obj.delete()
#         return JsonResponse({'success': True}, status=200)


class CommonViewSet(PaginateByMaxMixin, ModelViewSet):
    """ provide list/retrive/patch/delete restful api for model """
    max_paginate_by = 200
    filter_backends = (filters.SearchFilter,
                       filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    permission_classes = [permissions.DjangoModelPermissions]

    @list_route(methods=['post', 'delete'])
    def delete(self, request, pk=None):
        """ for batch delete """
        pk = request.DATA.get('pk')
        pk = pk.split(',')
        objects = self.queryset.filter(pk__in=pk)
        for obj in objects:
            obj.delete()
        return JsonResponse({'success': True}, status=200)
#
# class AbstractViewSet(PaginateByMaxMixin, ModelViewSet):
#     """ provide list/retrive/patch/delete restful api for model """
#     max_paginate_by = 200
#     filter_backends = (filters.SearchFilter,
#                        filters.DjangoFilterBackend,
#                        filters.OrderingFilter)
#     permission_classes = [permissions.DjangoModelPermissions]
#
#     def get_queryset(self):
#         if 'app_name' not in self.kwargs or 'model_name' not in self.kwargs:
#             raise SuspiciousOperation('CommonView cant get app_name and model_name.')
#
#         app_name = self.kwargs.get('app_name').lower()
#         model_name = self.kwargs.get('model_name').lower()
#         try:
#             model_content_type = ContentType.objects.get(app_label=app_name, model=model_name)
#         except ObjectDoesNotExist:
#             raise ViewDoesNotExist
#
#         self.queryset=model_content_type.model_class().objects.all()
#         self.serializer_class = model_content_type.model_class()._meta.serializer_class
#         return self.queryset
#
#
#     @list_route(methods=['post', 'delete'])
#     def delete(self, request, pk=None):
#         """ for batch delete """
#         pk = request.DATA.get('pk')
#         pk = pk.split(',')
#         objects = self.queryset.filter(pk__in=pk)
#         for obj in objects:
#             obj.delete()
#         return JsonResponse({'success': True}, status=200)