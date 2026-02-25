from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import City, TimeStampedModel
from apps.core.validators import validate_file_size


class UserProfile(TimeStampedModel):
    ROLE_USER = 'user'
    ROLE_ORGANIZER = 'organizer'
    ROLE_STAFF = 'staff'

    ROLE_CHOICES = [
        (ROLE_USER, _('Пользователь')),
        (ROLE_ORGANIZER, _('Организатор')),
        (ROLE_STAFF, _('Сотрудник')),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    role = models.CharField(_('Роль'), max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Город'))
    phone = models.CharField(_('Телефон'), max_length=30, blank=True)
    bio = models.TextField(_('О себе'), blank=True)
    avatar = models.ImageField(
        _('Аватар'),
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_file_size],
    )

    class Meta:
        ordering = ['user__username']
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')

    def __str__(self) -> str:
        return f"{self.user.username}"
