from django.contrib import admin

from apps.organizers.models import Organizer, OrganizerMember


class OrganizerMemberInline(admin.TabularInline):
    model = OrganizerMember
    extra = 1


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OrganizerMemberInline]


@admin.register(OrganizerMember)
class OrganizerMemberAdmin(admin.ModelAdmin):
    list_display = ('organizer', 'user', 'role', 'is_owner')
    list_filter = ('is_owner',)
    search_fields = ('organizer__name', 'user__username')
