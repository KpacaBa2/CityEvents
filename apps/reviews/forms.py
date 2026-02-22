from django import forms

from apps.reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'data-counter': 'reviewCounter', 'rows': 4}),
        }
