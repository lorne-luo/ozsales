# coding=utf-8
import inspect

from django.contrib import messages
from django.db import models

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ProfileRequiredMixin(LoginRequiredMixin):
    profile_required = []

    def check_perm(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return False

        profile_class_name = '%s.%s' % (request.profile._meta.app_label, request.profile._meta.model_name)
        for profile in self.profile_required:
            if isinstance(profile, str) and profile.lower() == profile_class_name:
                return True
            elif inspect.isclass(profile) and issubclass(profile, models.Model) and isinstance(request.profile,
                                                                                               profile):
                return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if self.check_perm(request, *args, **kwargs):
            return super(ProfileRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class PremiumSellerRequiredMixin(ProfileRequiredMixin):
    profile_required = ('member.seller',)

    def check_perm(self, request, *args, **kwargs):
        if super(PremiumSellerRequiredMixin, self).check_perm(request, *args, **kwargs):
            return request.profile.check_premium_member()
        else:
            return False

    def handle_no_permission(self):
        messages.warning(self.request, u'没有权限访问，请加入高级会员.')
        return HttpResponseRedirect(reverse_lazy('payments:add_card'))