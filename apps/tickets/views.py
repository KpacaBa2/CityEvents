from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.tickets.models import Ticket


@login_required
def my_tickets(request):
    tickets = (
        Ticket.objects.select_related('ticket_type__event')
        .filter(user=request.user)
        .order_by('-created_at')
    )
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})
