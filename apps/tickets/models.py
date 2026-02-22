import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.events.models import Event


class TicketType(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quota = models.PositiveIntegerField(default=0)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['price']
        unique_together = ('event', 'name')

    def __str__(self) -> str:
        return f"{self.event.title} - {self.name}"


class Ticket(TimeStampedModel):
    STATUS_NEW = 'new'
    STATUS_USED = 'used'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_USED, 'Used'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT, related_name='tickets')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.ticket_type}"
