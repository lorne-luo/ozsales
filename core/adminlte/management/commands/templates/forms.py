FORMS_HEADER = '''# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import <% ALL_MODELS %>

'''
FORMS_MODEL_TEMPLATE = '''
class <% MODEL_NAME %>AddForm(ModelForm):
    """ Add form for <% MODEL_NAME %> """
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>DetailForm(ModelForm):
    """ Detail form for <% MODEL_NAME %> """
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>UpdateForm(ModelForm):
    """ Update form for <% MODEL_NAME %> """
    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''