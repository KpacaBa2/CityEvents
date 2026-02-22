from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.events.models import Event
from apps.favorites.models import Favorite


@login_required
@require_POST
def toggle_favorite(request, slug):
    event = get_object_or_404(Event, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, event=event)
    if not created:
        favorite.delete()
        messages.info(request, _('Удалено из избранного.'))
    else:
        messages.success(request, _('Добавлено в избранное.'))
    return redirect('events:detail', slug=slug)


@login_required
def favorite_list(request):
    events_qs = Event.objects.annotate(
        avg_rating=Avg('reviews__rating', distinct=True),
        reviews_count=Count('reviews', distinct=True),
    )
    favorites = Favorite.objects.filter(user=request.user).prefetch_related(
        Prefetch('event', queryset=events_qs),
    )
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})
