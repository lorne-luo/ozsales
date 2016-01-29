FORMS_HEADER = '''from django import forms
from models import <% ALL_MODELS %>

'''
FORMS_MODEL_TEMPLATE = '''
class <% MODEL_NAME %>AddForm(forms.ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>UpdateForm(forms.ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>DetailForm(forms.ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''