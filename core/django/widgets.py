# coding=utf-8
from django import forms

class ImageInlineInput(forms.ClearableFileInput):
    template_name = 'widgets/image_file_input.html'
    input_text=u'更换'
    initial_text=u'当前'