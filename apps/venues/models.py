from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import City, TimeStampedModel
from apps.core.validators import validate_file_size


class Amenity(models.Model):
    name = models.CharField(_('Название'), max_length=80, unique=True)
    icon = models.CharField(_('Иконка'), max_length=120, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Удобство')
        verbose_name_plural = _('Удобства')

    def __str__(self) -> str:
        return self.name


class Venue(TimeStampedModel):
    name = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Слаг'), max_length=220, unique=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('Город'))
    address = models.CharField(_('Адрес'), max_length=255)
    capacity = models.PositiveIntegerField(_('Вместимость'), default=0, validators=[MinValueValidator(0)])
    description = models.TextField(_('Описание'), blank=True)
    map_url = models.URLField(_('Ссылка на карту'), blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='venues', verbose_name=_('Удобства'))
    cover = models.ImageField(
        _('Обложка'),
        upload_to='venues/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Площадка')
        verbose_name_plural = _('Площадки')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class VenuePhoto(TimeStampedModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='photos', verbose_name=_('Площадка'))
    image = models.ImageField(
        _('Изображение'),
        upload_to='venues/photos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )
    caption = models.CharField(_('Подпись'), max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Фото площадки')
        verbose_name_plural = _('Фото площадок')

    def __str__(self) -> str:
        return f"{self.venue.name}"
