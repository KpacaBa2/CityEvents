from django.contrib import admin

from apps.tickets.models import Ticket, TicketType


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'price', 'quota')
    list_filter = ('event',)
    search_fields = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_type', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('code',)
