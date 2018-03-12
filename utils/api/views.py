""" Base API view classes shared by apps. """
import ast
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
# from guardian.shortcuts import get_objects_for_user
from rest_framework import generics, viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError
from rest_framework_extensions.mixins import PaginateByMaxMixin

logger = logging.getLogger(__name__)
MAX_ITEMS = 100


class PaginateMaxModelViewSet(PaginateByMaxMixin, viewsets.ModelViewSet):
    """ ModelViewSet which allows ?limit=max to show all records. """
    max_paginate_by = MAX_ITEMS


class PaginateMaxReadOnlyModelViewSet(PaginateByMaxMixin,
                                      viewsets.ReadOnlyModelViewSet):
    """ ReadOnlyModelViewSet which allows ?limit=max to show all records. """
    max_paginate_by = MAX_ITEMS


class PaginateMaxReadUpdateDeleteModelViewSet(PaginateByMaxMixin,
                                              mixins.RetrieveModelMixin,
                                              mixins.UpdateModelMixin,
                                              mixins.DestroyModelMixin,
                                              mixins.ListModelMixin,
                                              viewsets.GenericViewSet):
    """ Does not allow to create records, only GET, PUT, PATCH + pagination. """
    max_paginate_by = MAX_ITEMS


class PaginateMaxListAPIView(PaginateByMaxMixin, generics.ListAPIView):
    """ ListApiView which allows ?limit=max to show all records. """
    max_paginate_by = MAX_ITEMS


class ContentTypeObjectView(GenericAPIView):
    """
     Abstract base view for identifying an object in a url like: .../<content_type_name>/<pk>
     The view will allow access based on the object of interest and independent
     of the model it actually creates/returns.
     e.g. to read/set Tags of a UserVideo the user needs object permission to
     view/change the UserVideo not to view/change Tags.
    """

    def get_queryset(self):
        if 'content_type_name' not in self.kwargs or 'pk' not in self.kwargs:
            raise ParseError('bad request, missed parameter content_type_name and pk')

        content_type_name = self.kwargs.get('content_type_name')
        try:
            content_type = ContentType.objects.get(model=content_type_name)
            return content_type.model_class().objects.all()
        except ContentType.DoesNotExist:
            error_detail = "No content type with name '%s' found." % content_type_name
            logger.error(error_detail)
            raise ParseError(error_detail)


class SharedObjectsList(PaginateMaxListAPIView):
    """
     Show list of one model's objects which are shared with current user.
     Set ?use_groups=False if you want to exclude objects which are not shared
     with the user itself but only with one of his groups.
    """

    def get_queryset(self):
        use_groups = self.request.GET.get('use_groups')
        if use_groups != None:
            try:
                # Turn string 'False' or 'True' to boolean
                use_groups = ast.literal_eval(use_groups)
            except ValueError:
                logger.info("Invalid parameter for use_groups, use 'True' or 'False'.")
                use_groups = True
        else:
            use_groups = True

        contenttype = ContentType.objects.get_for_model(self.model)
        view_perm = "%s.view_%s" % (contenttype.app_label, self.model.__name__.lower())

        objects = None
        # objects = get_objects_for_user(self.request.user, [view_perm],
        #                                klass=self.model,
        #                                use_groups=use_groups)

        return objects
