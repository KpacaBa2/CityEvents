from django.db.models import Avg, Count
from django.shortcuts import render

from apps.categories.models import Category
from apps.events.models import Event
from apps.venues.models import Venue


def home(request):
    events = (
        Event.objects.select_related('venue', 'organizer')
        .prefetch_related('categories', 'tags')
        .filter(status=Event.STATUS_PUBLISHED)
        .annotate(
            avg_rating=Avg('reviews__rating', distinct=True),
            reviews_count=Count('reviews', distinct=True),
        )
        .order_by('start_at')[:6]
    )
    return render(request, 'pages/home.html', {'events': events})


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def faq(request):
    return render(request, 'pages/faq.html')


def stats(request):
    categories = Category.objects.annotate(event_count=Count('events')).order_by('-event_count')
    venues = Venue.objects.annotate(event_count=Count('events')).order_by('-event_count')
    return render(request, 'pages/stats.html', {'categories': categories, 'venues': venues})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)
