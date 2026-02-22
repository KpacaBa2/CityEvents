from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.events.models import Event
from apps.reviews.forms import ReviewForm


@login_required
def add_review(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            messages.success(request, _('Отзыв сохранён.'))
            return redirect('events:detail', slug=slug)
        messages.error(request, _('Исправьте ошибки формы.'))
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'event': event})
