import copy
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pypinyin import pinyin, lazy_pinyin, Style


class PinYinFieldModelMixin(object):
    pinyin_field = 'pinyin'
    pinyin_fields_conf = []
    _original_fields_value = {}
    SPLITER = '|'

    def __init__(self, *args, **kwargs):
        super(PinYinFieldModelMixin, self).__init__(*args, **kwargs)
        field_names = [field_name for field_name, style, heteronym in self.pinyin_fields_conf]
        for field_name in set(field_names):
            self._original_fields_value.update({field_name: getattr(self, field_name)})

    def save(self, *args, **kwargs):
        self.update_pinyin_fields()
        super(PinYinFieldModelMixin, self).save(*args, **kwargs)

    def check_update(self):
        if not getattr(self, self.pinyin_field):
            return True
        for field_name, style, heteronym in self.pinyin_fields_conf:
            current_value = getattr(self, field_name)
            if current_value != self._original_fields_value.get(field_name) != None:
                return True

    def update_pinyin_fields(self):
        if self.check_update():
            setattr(self, self.pinyin_field, '')
            for field_name, style, heteronym in self.pinyin_fields_conf:
                current_value = getattr(self, field_name)
                new_pinyin = getattr(self, self.pinyin_field) + self.get_pinyin(current_value, style, heteronym)
                setattr(self, self.pinyin_field, new_pinyin)

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
