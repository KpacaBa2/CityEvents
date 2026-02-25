from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.categories.models import Category


class CategoryForm(forms.ModelForm):
    slug = forms.SlugField(required=False, label=_('Слаг'))

    class Meta:
        model = Category
        fields = ('name', 'slug', 'description')

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            return slug
        return slugify(self.cleaned_data.get('name', ''))
