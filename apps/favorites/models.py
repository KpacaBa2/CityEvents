from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.events.models import Event


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user} - {self.event}"
