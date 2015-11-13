''' Base API field classes shared by apps. '''
from datetime import datetime
import json
import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import timezone
from django.template.defaultfilters import date as _date
from taggit.models import Tag
from rest_framework import serializers

from utils.templatetags.humanize_timesince import humanize_timesince


log = logging.getLogger(__name__)

class RelativeDateTimeField(serializers.Field):
    '''
     Serialize a object's datetime field as their age, e.g. '2 days ago'.
    '''
    def field_to_native(self, obj, field_name):
        value = getattr(obj, self.source)
        if value:
            return humanize_timesince(value)
        return None


class LocalDateTimeField(serializers.Field):
    ''' Return field's value formated in local timezone. '''
    def field_to_native(self, obj, field_name):
        date = getattr(obj, self.source, None)
        if date:
            date = _date(timezone.localtime(getattr(obj, self.source)),
                         settings.SHORT_DATETIME_FORMAT).replace('p.m.', 'pm').replace('a.m.', 'am')
        return date

'''
TODO: Date format has to be in sync between backend/front (this may be nessesary for internalization):
        - to_native
        - js widgets (ie datetimepicker)
        - from_native
'''
class DateTimeLocalizeField(serializers.DateTimeField):

    def from_native(self, value):
        if not value:
            return None
        try:
            date = datetime.strptime(value, '%s %s' % (settings.DATE_INPUT_FORMAT,
                                                       settings.TIME_INPUT_FORMAT))
        except ValueError:
            raise serializers.ValidationError("Value '%s' does not match the date format. "
                                              "Expecting format like: 19/06/2015 2:16 pm"
                                              % value)
        else:
            value = timezone.get_current_timezone().localize(date)
        return super(DateTimeLocalizeField, self).from_native(value)

    def to_native(self, value):
        if not value:
            return None
        value = _date(timezone.localtime(value), settings.SHORT_DATETIME_FORMAT)
        return super(DateTimeLocalizeField, self).to_native(value)


class DateLocalizeField(DateTimeLocalizeField):
    ''' Takes a dd/mm/yyyy, stores it at current timezone's midnite of that date. '''
    def from_native(self, value):
        # Add midnite to given date (since a date itself cannot be timezoneware):
        if value:
            value += " 12:00 AM"
        return super(DateLocalizeField, self).from_native(value)


class DisplayNestedFKField(serializers.Field):
    """
     Returns representation of a nested FK as it's serializer would do,
     since that however breaks write-options with current restframework version,
     we use this on an extra display-only field, e.g. encoding_job_display

     https://github.com/tomchristie/django-rest-framework/issues/395
    """
    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        self.read_only = True
        super(DisplayNestedFKField, self).__init__(*args, **kwargs)

    def field_to_native(self, obj, field_name):
        """
        Use serializer passed to __init__() to serialize the model's field.

        :param obj:
        :param field_name:
        :return:
        """
        foreign_key = getattr(obj, self.source, None)
        if foreign_key:
            if getattr(foreign_key, 'all', False) and callable(foreign_key.all):
                # M2M, serialize all (make sure to return empty list and not None
                # if it does not have any)
                foreign_key = foreign_key.all()
                fk_objs = self.serializer(foreign_key, many=True).data
                for obj in fk_objs:
                    if obj.get(u'content_type'):
                        del(obj[u'content_type'])
                return fk_objs
            else:
                obj = self.serializer(foreign_key).data
                if obj.get(u'content_type'):
                    del(obj[u'content_type'])
                return obj


class TagsField(serializers.Field):
    ''' List of tags of the object '''

    def field_to_native(self, obj, field_name):
        if callable(getattr(obj, 'cast', False)):
            obj = obj.cast()

        tags = Tag.objects.filter(
            taggit_taggeditem_items__content_type=ContentType.objects.get_for_model(obj),
            taggit_taggeditem_items__object_id=obj.pk).values_list('name', flat=True)
        return tags


class TypeField(serializers.Field):
    def field_to_native(self, obj, field_name):
        '''
         Class name of the object e.g. RecordingVideo, will try to cast it
         to a child class if available.
        '''
        if callable(getattr(obj, 'cast', False)):
            obj = obj.cast()

        return type(obj).__name__


class DetailUrlField(serializers.Field):
    def field_to_native(self, obj, field_name):
        '''
         API url for detail view of object (implies that url follows naming
         convention of ModelViewsets)
        '''
        if callable(getattr(obj, 'cast', False)):
            obj = obj.cast()

        try:
            url = reverse('api:%s-detail' % type(obj).__name__.lower(), args=[obj.pk])
        except NoReverseMatch:
            url = None
        return url


class MediaUrlField(serializers.Field):
    '''
     Returns a uploaded file's url as needed for referencing it on the
     frontend (= including the MEDIA_URL part).
    '''

    def to_native(self, obj):
        return obj and obj.url or None


class VariationImageAPIField(serializers.ImageField):
    def validate(self, value, *args, **kwargs):
        '''
         Calls validation from the actual model field (StdImageField) in-time
         to avoid 500 error.
        '''
        # For small files django uses InMemoryUploadedFile where it's easy to
        # get the field name, for big files it uses TemporaryUploadedFile.
        # where it's a bit hacky to achive the same (would work for
        # InMemoryUploadedFile too though):
        field_name = getattr(value, 'field_name',
                             self.root.fields.keys()[self.root.fields.values().index(self)])

        super(VariationImageAPIField, self).validate(value)
        if value:
            self.parent.Meta.model._meta.get_field(field_name).validate(value, None)


class VariationUrlField(serializers.Field):
    ''' Provides urls to all image variations. '''
    @staticmethod
    def to_native(value):
        variations = {}
        if value:
            for name, _specs in settings.THUMBNAIL_VARIATIONS.items():
                variations[name] = getattr(value, name).url
        return variations


class FormDataPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
     Custom PrimaryKeyRelatedField which allows clearing a M2M relation defined
     on the related model when using a FormData object (e.g user's group
     membership). An empty string will clear the field.
    """
    def field_from_native(self, data, files, field_name, into):
        data = dict(data)
        if self.many:
            if data.get(field_name) == ['']:
                data[field_name] = []

        super(FormDataPrimaryKeyRelatedField, self).field_from_native(
            data, files, field_name, into)


class AjaxUploadImageField(serializers.ModelField):
    """
    A custom field to use with an ajax uploaded image
    """
    def field_to_native(self, obj, field_name):
        value = self.model_field._get_val_from_obj(obj)
        return value.url if len(value) else value

    def field_from_native(self, data, files, field_name, into):
        return super(AjaxUploadImageField, self).field_from_native(data, files, field_name, into)

    def from_native(self, value):
        if value.startswith(settings.MEDIA_URL):
            # Strip and media url to determine the path relative to media root
            value = value[len(settings.MEDIA_URL):]
        return super(AjaxUploadImageField, self).from_native(value)


class FittedWidgetImageField(serializers.Field):
    ''' Returns url to image fitted to its widget (hacky)'''
    def field_to_native(self, obj, field_name):
        return obj.get_fitted_image_url()


# class MultipleChoiceField(serializers.WritableField):
#     """
#     A field that behaves like multiple choice field of Django forms.
#     """
#     def from_native(self, data):
#         # Try to deserialize str (cant figure out why using 'httpie' on terminal
#         # makes data arrives as python here while jquery's as str):
#         if isinstance(data, basestring):
#             data = json.loads(data)
#
#         if isinstance(data, list):
#             for item in data:
#                 if not item in self.choices:
#                     raise serializers.ValidationError("The item you entered is not in the allowed items list.")
#             return data
#         else:
#             raise serializers.ValidationError("Please provide a valid list.")
#
#     def to_native(self, value):
#         return value
#
#     def __init__(self, choices=None, *args, **kwargs):
#         self.choices = dict(choices)
#         super(MultipleChoiceField, self).__init__(*args, **kwargs)
#
#     def to_internal_value(self, data):
#         data = data.strip('rgb(').rstrip(')')
#         red, green, blue = [int(col) for col in data.split(',')]
#         return Color(red, green, blue)

class JSONField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        json_data = {}
        try:
            json_data = json.loads(data)
        except ValueError, e:
            pass
        finally:
            return json_data
    def to_representation(self, value):
        return value
