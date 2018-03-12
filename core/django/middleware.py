#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.contrib.auth.middleware import AuthenticationMiddleware

__author__ = 'lorne'


class ProfileAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super(ProfileAuthenticationMiddleware, self).process_request(request)
        profile = getattr(request.user, 'profile', None)
        setattr(request, 'profile', profile)
