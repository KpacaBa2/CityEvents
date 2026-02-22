from django import forms
from django.utils.text import slugify

from apps.events.models import Event


class EventForm(forms.ModelForm):
    slug = forms.SlugField(required=False)

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
