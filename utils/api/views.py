''' Base API view classes shared by apps. '''
import ast
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework_extensions.mixins import PaginateByMaxMixin

log = logging.getLogger(__name__)
MAX_ITEMS = 100

class PaginateMaxModelViewSet(PaginateByMaxMixin, viewsets.ModelViewSet):
    ''' ModelViewSet which allows ?limit=max to show all records. '''
    max_paginate_by = MAX_ITEMS


class PaginateMaxReadOnlyModelViewSet(PaginateByMaxMixin,
                                      viewsets.ReadOnlyModelViewSet):
    ''' ReadOnlyModelViewSet which allows ?limit=max to show all records. '''
    max_paginate_by = MAX_ITEMS


class PaginateMaxReadUpdateDeleteModelViewSet(PaginateByMaxMixin,
                                              mixins.RetrieveModelMixin,
                                              mixins.UpdateModelMixin,
                                              mixins.DestroyModelMixin,
                                              mixins.ListModelMixin,
                                              viewsets.GenericViewSet):
    ''' Does not allow to create records, only GET, PUT, PATCH + pagination. '''
    max_paginate_by = MAX_ITEMS


class PaginateMaxListAPIView(PaginateByMaxMixin, generics.ListAPIView):
    ''' ListApiView which allows ?limit=max to show all records. '''
    max_paginate_by = MAX_ITEMS


class ContentTypeObjectView(APIView):
    '''
     Abstract base view for identifying an object in a url like: .../<content_type>/<pk>
     The view will allow access based on the object of interest and independent
     of the model it actually creates/returns.
     e.g. to read/set Tags of a UserVideo the user needs object permission to
     view/change the UserVideo not to view/change Tags.
    '''
    def identify_object(self):
        ''' Get object (access permissions are already checked at this point) '''
        content_type_name = self.kwargs.get('content_type')
        object_id = self.kwargs.get('pk')
        try:
            self.content_type = ContentType.objects.get(model=content_type_name)
            return self.content_type.model_class().objects.get(pk=object_id)
        except ContentType.DoesNotExist:
            log.error("No content type with name '%s' found." % content_type_name)
            raise Http404
        except ObjectDoesNotExist:
            log.error("Object with id '%s' and content type name '%s' not found."
                      % (object_id, content_type_name))
            raise Http404

