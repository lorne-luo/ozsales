from dal_select2.widgets import Select2WidgetMixin, ModelSelect2, Select2
from dal.widgets import QuerySetSelectMixin
from django import forms


class FormsetSelect2WidgetMixin(Select2WidgetMixin):
    """Mixin for Select2 widgets."""

    class Media:
        """Automatically include static files for the admin."""

        css = {
            'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.css',
                'autocomplete_light/select2.css',
            )
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'js/autocomplete_light/autocomplete.init.js',  # hacked this
            'autocomplete_light/vendor/select2/dist/js/select2.full.js',
            'autocomplete_light/select2.js',
        )

    autocomplete_function = 'select2'


class FormsetModelSelect2(QuerySetSelectMixin,
                          FormsetSelect2WidgetMixin,
                          forms.Select):
    pass
