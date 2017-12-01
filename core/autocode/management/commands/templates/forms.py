FORMS_HEADER = '''# coding=utf-8
from django import forms
from models import <% ALL_MODELS %>

'''
FORMS_MODEL_TEMPLATE = '''
class <% MODEL_NAME %>AddForm(forms.ModelForm):
    """ Add form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>DetailForm(forms.ModelForm):
    """ Detail form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>UpdateForm(forms.ModelForm):
    """ Update form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''