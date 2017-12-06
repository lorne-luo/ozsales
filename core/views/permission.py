import inspect
from django.db import models

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class ProfileRequiredMixin(LoginRequiredMixin):
    profile_required = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        profile_class_name = '%s.%s' % (request.profile._meta.app_label, request.profile._meta.model_name)
        for profile in self.profile_required:
            if issubclass(profile, models.Model) and isinstance(request.profile, profile):
                return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
            elif isinstance(profile, str) and profile.lower() == profile_class_name:
                return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        return self.handle_no_permission()
