from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apps.organizers.models import OrganizerMember


class OrganizerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return True
        profile = getattr(user, 'userprofile', None)
        return bool(profile and profile.role in {'organizer', 'staff'})


class OrganizerMemberRequiredMixin(OrganizerRequiredMixin):
    def get_allowed_organizer_ids(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return None
        return OrganizerMember.objects.filter(user=user).values_list('organizer_id', flat=True)

    def get_queryset(self):
        qs = super().get_queryset()
        allowed_ids = self.get_allowed_organizer_ids()
        if allowed_ids is None:
            return qs
        return qs.filter(organizer_id__in=allowed_ids)
