from django.contrib import admin

from apps.events.models import Event, EventImage, EventSchedule


class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = ('event', 'start_at', 'end_at')
    list_filter = ('start_at',)
    search_fields = ('event__title',)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'created_at')
    search_fields = ('event__title', 'caption')


@admin.action(description='Mark selected events as published')
def mark_published(modeladmin, request, queryset):
    queryset.update(status=Event.STATUS_PUBLISHED)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at', 'status', 'venue', 'organizer')
    list_filter = ('status', 'start_at', 'venue')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventScheduleInline, EventImageInline]
    actions = [mark_published]
