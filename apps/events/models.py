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
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='events')
    organizer = models.ForeignKey(Organizer, on_delete=models.PROTECT, related_name='events')
    categories = models.ManyToManyField(Category, blank=True, related_name='events')
    tags = models.ManyToManyField(Tag, blank=True, related_name='events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    price_from = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_featured = models.BooleanField(default=False)
    max_attendees = models.PositiveIntegerField(default=0)
    cover = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['start_at']

    def clean(self):
        if self.end_at < self.start_at:
            raise ValidationError(_('Дата окончания должна быть позже даты начала.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class EventSchedule(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['start_at']

    def __str__(self) -> str:
        return f"{self.event.title}"


class EventImage(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='events/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.event.title}"
