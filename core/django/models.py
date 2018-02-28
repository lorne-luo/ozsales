import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from pypinyin import pinyin, Style


class PinYinFieldModelMixin(object):
    """
    add `pinyin` field in dest model, then inherit from this mixin, configure `pinyin_fields_conf`
    pinyin_fields_conf = [
            ('name_cn', Style.NORMAL, False), # original field, style,
        ]
    """
    pinyin_field = 'pinyin'
    pinyin_fields_conf = []
    _original_fields_value = {}
    SPLITER = '|'

    def __init__(self, *args, **kwargs):
        super(PinYinFieldModelMixin, self).__init__(*args, **kwargs)
        field_names = [field_name for field_name, style, heteronym in self.pinyin_fields_conf]
        for field_name in set(field_names):
            current_value = self.get_attr_by_str(field_name)
            self._original_fields_value.update({field_name: current_value})

    def save(self, *args, **kwargs):
        if self.check_update():
            self.update_pinyin_fields()
        super(PinYinFieldModelMixin, self).save(*args, **kwargs)

    def check_update(self):
        if not getattr(self, self.pinyin_field, None):
            return True
        for field_name, style, heteronym in self.pinyin_fields_conf:
            current_value = self.get_attr_by_str(field_name)
            if current_value != self._original_fields_value.get(field_name) != None:
                return True

    def update_pinyin_fields(self):
        # only update pinyin field when fields updated
        new_pinyin = ''
        for field_name, style, heteronym in self.pinyin_fields_conf:
            current_value = self.get_attr_by_str(field_name)
            new_pinyin += self.get_pinyin(current_value, style, heteronym)
            setattr(self, self.pinyin_field, new_pinyin.lower())

    @classmethod
    def get_pinyin(cls, value, style=Style.NORMAL, heteronym=False):
        if not value:
            return ''
        value = unicode(value)
        pylist = pinyin(value, style=style, heteronym=heteronym, strict=True)
        # example [[u'di', u'zhai'], [u'xiao'], [u'fei']]
        combinations = cls.get_combinations(pylist)

        full_pinyin = cls.SPLITER.join(combinations)
        result = '%s%s' % (cls.SPLITER, full_pinyin)
        return result

    @classmethod
    def get_combinations(cls, arr):
        if len(arr) == 1:
            return arr[0]
        result = []
        rest_combinations = cls.get_combinations(arr[1:])
        for ch in arr[0]:
            for combin in rest_combinations:
                result.append('%s%s' % (ch, combin))
        return result

    def get_attr_by_str(self, attr_name):
        obj = self
        attr_names = attr_name.split('.')
        for name in attr_names:
            obj = getattr(obj, name, None)
            if obj is None:
                return None
        return obj


class ResizeUploadedImageModelMixin(object):
    """
    resize image when first uploaded
    usage:
        cal self.resize_image('image_field_name') before super.save()
    """
    MAX_WIDTH = 800

    def resize_image(self, image_field_name):
        # resize uploaded image when save new
        image = getattr(self, image_field_name)
        if not image:
            return
        try:
            file = image.file
        except:
            return

        if isinstance(file, InMemoryUploadedFile):
            im = Image.open(image)
            width, height = im.size
            if width > self.MAX_WIDTH:
                new_height = int(float(self.MAX_WIDTH) / width * height)
                output = BytesIO()
                # Resize/modify the image
                im = im.resize((self.MAX_WIDTH, new_height))
                # after modifications, save it to the output
                im.save(output, format='JPEG', quality=70)
                output.seek(0)
                # change the imagefield value to be the newley modifed image value
                setattr(self, image_field_name, InMemoryUploadedFile(
                    output, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                    'image/jpeg', sys.getsizeof(output), None))
