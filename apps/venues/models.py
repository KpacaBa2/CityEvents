from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from apps.core.models import City, TimeStampedModel
from apps.core.validators import validate_file_size


class Amenity(models.Model):
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Venue(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='venues')
    cover = models.ImageField(
        upload_to='venues/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class VenuePhoto(TimeStampedModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(
        upload_to='venues/photos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.venue.name}"
