# coding=utf-8
from dal_select2.widgets import Select2WidgetMixin
from dal.widgets import QuerySetSelectMixin
from django import forms


class FormsetSelect2WidgetMixin(Select2WidgetMixin):
    """Mixin for Select2 widgets."""

    class Media:
        """Automatically include static files for the admin."""

        css = {
            'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.min.css',
                'autocomplete_light/select2.css',
            )
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'js/autocomplete_light/autocomplete.init.min.js',  # hacked this
            'autocomplete_light/vendor/select2/dist/js/select2.full.min.js',
            'autocomplete_light/select2.js',
            # Provide an additional i18 js.
            'autocomplete_light/vendor/select2/dist/js/i18n/zh-CN.js',
        )

    autocomplete_function = 'select2'

    def build_attrs(self, *args, **kwargs):
        attrs = super(FormsetSelect2WidgetMixin, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-language', 'zh-CN')
        return attrs

class FormsetModelSelect2(QuerySetSelectMixin,
                          FormsetSelect2WidgetMixin,
                          forms.Select):
    pass

class HansSelect2ViewMixin(object):
    # translate into chinese
    def get_create_option(self, context, q):
        create_option = super(HansSelect2ViewMixin, self).get_create_option(context, q)
        if create_option:
            create_option[0]['text'] = u'点击新建 "%s"' % q
        return create_option
