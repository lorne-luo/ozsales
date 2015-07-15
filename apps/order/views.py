from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User, Group, AnonymousUser
from django.db.models import Q
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.utils.http import urlquote, urlunquote
from django.conf import settings
from django.core.urlresolvers import reverse
from models import Order


def change_order_status(request, order_id, status_str):
    order = get_object_or_404(Order, pk=order_id)
    if order:
        order.status = status_str
        order.save()

    return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % ('order', 'order')))