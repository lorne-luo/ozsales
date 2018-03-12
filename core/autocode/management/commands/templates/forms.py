FORMS_HEADER = '''# coding=utf-8
from django import forms
from .models import <% ALL_MODELS %>

'''
FORMS_BODY = '''
class <% MODEL_NAME %>AddForm(forms.ModelForm):
    """ Add form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>


class <% MODEL_NAME %>UpdateForm(<% MODEL_NAME %>AddForm):
    """ Update form for <% MODEL_NAME %> """
    pass


class <% MODEL_NAME %>DetailForm(forms.ModelForm):
    """ Detail form for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>

'''