FORMS_HEADER = '''# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import <% ALL_MODELS %>

'''
FORMS_MODEL_TEMPLATE = '''
class <% MODEL_NAME %>AddForm(ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>DetailForm(ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>UpdateForm(ModelForm):
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''