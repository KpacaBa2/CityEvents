from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.tickets.models import TicketType


class Order(TimeStampedModel):
    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Order #{self.pk}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['order_id']

    def __str__(self) -> str:
        return f"{self.order_id} - {self.ticket_type}"


class Payment(TimeStampedModel):
    PROVIDER_CARD = 'card'
    PROVIDER_CASH = 'cash'

    STATUS_NEW = 'new'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    provider = models.CharField(max_length=20, default=PROVIDER_CARD)
    status = models.CharField(max_length=20, default=STATUS_NEW)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    transaction_id = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Payment {self.order_id}"
