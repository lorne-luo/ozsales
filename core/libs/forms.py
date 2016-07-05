from django import forms
from django.utils.translation import ugettext_lazy as _


class ModelForm(forms.ModelForm):
    """
    remove the Hold down hint for manytomanyfield
    """
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        for field in self.base_fields:
            if self.base_fields[field].help_text:
                help_text=unicode(self.base_fields[field].help_text)
                help_text = help_text.replace(remove_message, '').strip()
                self.fields[field].help_text = help_text