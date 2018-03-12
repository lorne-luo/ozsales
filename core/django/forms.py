# coding=utf-8
import copy
from django import forms
from django.utils.translation import ugettext_lazy as _


class NoManytoManyHintModelForm(forms.ModelForm):
    """
    remove the Hold down hint for manytomanyfield
    """

    def __init__(self, *args, **kwargs):
        super(NoManytoManyHintModelForm, self).__init__(*args, **kwargs)
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        for field_name in self.base_fields:
            if self.base_fields[field_name].help_text:
                help_text = self.base_fields[field_name].help_text
                help_text = help_text.replace(remove_message, '').strip()
                self.fields[field_name].help_text = help_text

            field = self.fields.get(field_name)
            if type(field.widget) in [forms.SelectMultiple]:
                field.widget.attrs['placeholder'] = u'可多选'
            else:
                if field.help_text:
                    field.widget.attrs['placeholder'] = field.help_text
                elif field.required:
                    field.widget.attrs['placeholder'] = u'必填'
                else:
                    field.widget.attrs['placeholder'] = u'可选'


class ReadonlyModelFormMixin(object):
    readonly_exclude = ()

    def get_update_fields(self):
        # exclude field not belong this model from
        update_fields = copy.deepcopy(self.readonly_exclude)
        fields_name = [field.name for field in self.instance._meta.get_fields()]
        for field in self.readonly_exclude:
            if field not in fields_name:
                update_fields.remove(field)

        return update_fields

    def __init__(self, *args, **kwargs):
        super(ReadonlyModelFormMixin, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key in self.readonly_exclude:
                continue

            # .disabled is new attr in Django 1.9, will ignore this field when submit, so no worry about html tamper
            field.disabled = True
            field.widget.attrs['readonly'] = True
            field.required = False

    def save(self, commit=True):
        if self.readonly_exclude:
            if self.errors:
                raise ValueError(
                    "The %s could not be %s because the data didn't validate." % (
                        self.instance._meta.object_name,
                        'created' if self.instance._state.adding else 'changed',
                    )
                )
            if commit:
                self.instance.save(update_fields=self.get_update_fields())
                self._save_m2m()
            else:
                self.save_m2m = self._save_m2m
            return self.instance
        else:
            # without saving
            return self.instance
