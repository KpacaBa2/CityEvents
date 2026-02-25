from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(_('Название'), max_length=120, unique=True)
    slug = models.SlugField(_('Слаг'), max_length=140, unique=True)
    description = models.TextField(_('Описание'), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
