# coding=utf-8
from django import forms


class ThumbnailImageInput(forms.ClearableFileInput):
    template_name = 'widgets/thumbnail_image_file_input.html'
    input_text = u'更换'
    initial_text = u'当前'
    width = None
    height = None
    size = None

    def __init__(self, attrs=None):
        """
        size: large|medium|thumbnail|None(original)
        """
        if attrs:
            self.width = attrs.pop('width', None)
            self.height = attrs.pop('height', None)
            self.size = attrs.pop('size', None)
        super(ThumbnailImageInput, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        if value:
            if self.size == 'thumbnail':
                value = value.thumbnail
            elif self.size == 'medium':
                value = value.medium
            elif self.size == 'large':
                value = value.large

        context = super(ThumbnailImageInput, self).get_context(name, value, attrs)
        context['widget'].update({
            'width': self.width,
            'height': self.height,
        })
        return context
