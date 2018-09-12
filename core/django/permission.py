# coding=utf-8
import inspect

from django.contrib import messages
from django.db import models

from django.contrib.auth.mixins import LoginRequiredMixin
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


class SellerRequiredMixin(ProfileRequiredMixin):
    profile_required = ('member.seller',)


class CustomerRequiredMixin(ProfileRequiredMixin):
    profile_required = ('customer.customer',)


class PremiumSellerRequiredMixin(ProfileRequiredMixin):
    profile_required = ('member.seller',)

    def check_perm(self, request, *args, **kwargs):
        if super(PremiumSellerRequiredMixin, self).check_perm(request, *args, **kwargs):
            return request.profile.is_premium
        else:
            return False

    def handle_no_permission(self):
        messages.warning(self.request, '没有权限访问，请加入高级会员.')
        return HttpResponseRedirect(reverse_lazy('payments:add_card'))


class SellerOwnerOrSuperuserRequiredMixin(ProfileRequiredMixin):
    """
    for update and detail view only, check pk
    """
    raise_exception = True
    superuser_allowed = True
    profile_required = ('member.seller',)

    def check_perm(self, request, *args, **kwargs):
        if self.superuser_allowed and self.request.user.is_superuser:
            return True

        if super(SellerOwnerOrSuperuserRequiredMixin, self).check_perm(request, *args, **kwargs):
            pk = kwargs.get('pk')
            if not pk:
                # equal to ProfileRequiredMixin
                return True
            else:
                return self.model.objects.filter(pk=pk, seller=self.request.profile).exists()
        return False


class SellerOwnerOnlyRequiredMixin(SellerOwnerOrSuperuserRequiredMixin):
    superuser_allowed = False
