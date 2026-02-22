from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.core.models import City, TimeStampedModel
from apps.core.validators import validate_file_size


class UserProfile(TimeStampedModel):
    ROLE_USER = 'user'
    ROLE_ORGANIZER = 'organizer'
    ROLE_STAFF = 'staff'

    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ORGANIZER, 'Organizer'),
        (ROLE_STAFF, 'Staff'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['user__username']

    def __str__(self) -> str:
        return f"{self.user.username}"
