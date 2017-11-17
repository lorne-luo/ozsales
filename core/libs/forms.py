# coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _


class ModelForm(forms.ModelForm):
    """
    remove the Hold down hint for manytomanyfield
    """

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
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
                    field.widget.attrs['placeholder'] = u'选填'
