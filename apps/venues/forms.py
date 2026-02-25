from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.venues.models import Venue


class VenueForm(forms.ModelForm):
    slug = forms.SlugField(required=False, label=_('Слаг'))

    class Meta:
        model = Venue
        fields = ('name', 'slug', 'city', 'address', 'capacity', 'description', 'map_url', 'amenities', 'cover')

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug
        return slugify(self.cleaned_data.get('name', ''))
