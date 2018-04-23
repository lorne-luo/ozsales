# coding=utf-8
import os
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
        original_value = value
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
            'original_value': original_value,
            'download_filename': self.get_download_filename(original_value)
        })
        return context

    def get_download_filename(self, value):
        if value and value.path:
            filename = os.path.basename(value.path)
            return filename
        return None


class IDThumbnailImageInput(ThumbnailImageInput):
    def get_download_filename(self, value):
        if value:
            side = u'正面' if 'front' in value.field.name else u'反面'
            filename, file_ext = os.path.splitext(value.name)
            return '%s_%s%s' % (value.instance.name, side, file_ext)
        return super(IDThumbnailImageInput, self).get_download_filename(value)
