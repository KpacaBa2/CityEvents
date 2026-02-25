from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.events.models import Event


class Review(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Событие'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    rating = models.PositiveIntegerField(
        _('Оценка'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(_('Комментарий'), blank=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-created_at']
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self) -> str:
        return f"{self.event.title} - {self.rating}"
