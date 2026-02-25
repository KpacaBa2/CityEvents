from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.categories.models import Category
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_file_size
from apps.organizers.models import Organizer
from apps.tags.models import Tag
from apps.venues.models import Venue


class Event(TimeStampedModel):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Черновик')),
        (STATUS_PUBLISHED, _('Опубликовано')),
        (STATUS_CANCELLED, _('Отменено')),
    ]

    title = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Слаг'), max_length=220, unique=True)
    description = models.TextField(_('Описание'))
    start_at = models.DateTimeField(_('Дата начала'))
    end_at = models.DateTimeField(_('Дата окончания'))
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='events', verbose_name=_('Площадка'))
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.PROTECT,
        related_name='events',
        verbose_name=_('Организатор'),
    )
    categories = models.ManyToManyField(Category, blank=True, related_name='events', verbose_name=_('Категории'))
    tags = models.ManyToManyField(Tag, blank=True, related_name='events', verbose_name=_('Теги'))
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    price_from = models.DecimalField(
        _('Цена от'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    is_featured = models.BooleanField(_('Рекомендуемое'), default=False)
    max_attendees = models.PositiveIntegerField(_('Максимум участников'), default=0)
    cover = models.ImageField(
        _('Обложка'),
        upload_to='events/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['start_at']
        verbose_name = _('Событие')
        verbose_name_plural = _('События')

    def clean(self):
        if not self.start_at or not self.end_at:
            return
        if self.end_at < self.start_at:
            raise ValidationError({'end_at': _('Дата окончания должна быть позже даты начала.')})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class EventSchedule(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('Событие'))
    start_at = models.DateTimeField(_('Дата начала'))
    end_at = models.DateTimeField(_('Дата окончания'))
    note = models.CharField(_('Примечание'), max_length=200, blank=True)

    class Meta:
        ordering = ['start_at']
        verbose_name = _('Расписание')
        verbose_name_plural = _('Расписания')

    def __str__(self) -> str:
        return f"{self.event.title}"


class EventImage(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', verbose_name=_('Событие'))
    image = models.ImageField(
        _('Изображение'),
        upload_to='events/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )
    caption = models.CharField(_('Подпись'), max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Фото события')
        verbose_name_plural = _('Фото событий')

    def __str__(self) -> str:
        return f"{self.event.title}"
