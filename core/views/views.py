# coding=utf-8
from django.contrib.auth.views import password_change
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.core.exceptions import ViewDoesNotExist, ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView, TemplateView, DetailView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import PaginateByMaxMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route, list_route
from rest_framework import filters, permissions
from core.libs import constants

# from core.adminlte.models import Menu, SystemConfig, Permission
# from core.messageset.models import Notification, Task
# from core.organization.models import Staff

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
            'page_title': page_title.title(),
            'page_model': getattr(self, 'model', ''),
            'page_app_name': self.app_name,
            'page_model_name': self.model_name,
            'page_model_verbose_name': getattr(self, 'model')._meta.verbose_name.title(),
            'page_system_name': settings.SITE_NAME,
            'page_system_subhead': '',
            'page_model_perms': page_model_perms
        }
        context.update(common_dict)
        return context

    def get_success_url(self):
        if '_continue' in self.request.POST and self.object:
            url_tag = '%s:%s-update' % (self.app_name, self.model_name)
            return reverse(url_tag, args=[self.object.id])
        else:
            url_tag = '%s:%s-list' % (self.app_name, self.model_name)
            return reverse(url_tag)


class CommonPageViewMixin(object):
    model = None

    @property
    def app_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.app_label
        return ''

    @property
    def model_name(self):
        if getattr(self, 'model', None):
            return getattr(self, 'model')._meta.model_name
        return ''

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
        if getattr(self, 'model', None):
            page_title = getattr(self, 'model')._meta.verbose_name
        else:
            page_title = default_dashboard_title

        common_dict = {
            'default_dashboard_title': default_dashboard_title,
            'page_title': page_title,
            'page_model': getattr(self, 'model', ''),
            'page_app_name': getattr(self, 'app_name', ''),
            'page_model_name': getattr(self, 'model_name', ''),
            'page_system_name': settings.SITE_NAME,
            'page_system_subhead': ''
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

        if hasattr(self.model.Config, 'success_url'):
            self.success_url = self.model.Config.success_url
        else:
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
# permission_classes = [permissions.DjangoModelPermissions]
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
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    permission_classes = [permissions.DjangoModelPermissions]

    @list_route(methods=['post', 'delete'])
    def delete(self, request, pk=None):
        """ for batch delete """
        pk = request.DATA.get('pk')
        pk = pk.split(',')
        self.get_queryset().filter(pk__in=pk).delete()
        return JsonResponse({'success': True}, status=200)

    @list_route(methods=['post', 'get'])
    def page(self, request):
        """ pagenation api for jquery.dataTable """
        draw = request.GET.get('draw', 0)
        length = int(request.GET.get('length', 5))
        start = int(request.GET.get('start', 0))
        order_column = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')
        search_keyword = request.GET.get('search[value]', '')
        raise NotImplementedError
        # column_field_map = {
        #     0: 'start_time',
        #     1: 'title',
        #     2: 'start_time',
        #     3: 'end_time',
        #     4: 'version',
        #     5: 'parental_rating',
        # }
        # order_string = column_field_map[order_column]
        #
        # if order_direction.lower() == 'desc':
        #     order_string = '-' + order_string
        #
        # events = Event.objects.filter(channel_id=channel_id).order_by(order_string)
        # records_total = events.count()
        #
        # if search_keyword:
        #     events = events.filter(
        #         Q(title__icontains=search_keyword) | Q(parental_rating__abbreviation__icontains=search_keyword))
        # records_filtered_total = events.count()
        #
        # if length >= 0:
        #     events = events[start: start + length]
        #
        # data = []
        # for e in events:
        #     parental_rating_str = e.parental_rating.abbreviation if e.parental_rating else ''
        #     item = ['<input type="checkbox" name="selected_events" class="checkboxes" value="%s" />' % e.id,
        #             '<a href="%s">%s</a>' % (reverse('event-edit', kwargs={'event_id': e.id, }), e.title),
        #             formats.localize(timezone.localtime(e.start_time)),  # timezone convert and datetime string localize
        #             formats.localize(timezone.localtime(e.end_time)),
        #             parental_rating_str,
        #             EventRecordStatus.get_record_button(e, e.get_record_button_code(request.user))
        #             ]
        #     data.append(item)
        #
        # result = {
        #     "draw": draw,
        #     "length": len(data),
        #     "start": start,
        #     "end": start + length,
        #     "recordsTotal": records_total,
        #     "recordsFiltered": records_filtered_total,
        #     "data": data,
        #     "error": ""
        # }
        # return Response(result)


#
# class AbstractViewSet(PaginateByMaxMixin, ModelViewSet):
#     """ provide list/retrive/patch/delete restful api for model """
#     max_paginate_by = 200
#     filter_backends = (filters.SearchFilter,
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

