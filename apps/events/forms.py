from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.events.models import Event


class EventForm(forms.ModelForm):
    DATETIME_FORMAT = '%d.%m.%Y %H:%M'
    DATETIME_INPUT_FORMATS = (
        '%d.%m.%Y %H:%M',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M',
    )

    start_at = forms.DateTimeField(
        label=_('Дата начала'),
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_FORMAT,
            attrs={
                'class': 'js-datetime',
                'autocomplete': 'off',
                'placeholder': 'dd.mm.yyyy hh:mm',
            },
        ),
    )
    end_at = forms.DateTimeField(
        label=_('Дата окончания'),
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_FORMAT,
            attrs={
                'class': 'js-datetime',
                'autocomplete': 'off',
                'placeholder': 'dd.mm.yyyy hh:mm',
            },
        ),
    )
    slug = forms.SlugField(required=False, label=_('Слаг'))

    class Meta:
        model = Event
        fields = (
            'title', 'slug', 'description', 'start_at', 'end_at', 'venue',
            'organizer', 'categories', 'tags', 'status', 'price_from',
            'is_featured', 'max_attendees', 'cover'
        )

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug
        return slugify(self.cleaned_data.get('title', ''))


class EventSearchForm(forms.Form):
    q = forms.CharField(required=False)
    category = forms.CharField(required=False)
    city = forms.CharField(required=False)
    ordering = forms.CharField(required=False)
