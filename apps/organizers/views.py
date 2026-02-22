from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render

from apps.organizers.models import Organizer


def organizer_list(request):
    organizers = Organizer.objects.all()
    paginator = Paginator(organizers, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'organizers/organizer_list.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode()},
    )


def organizer_detail(request, slug):
    organizer = get_object_or_404(Organizer, slug=slug)
    events = organizer.events.annotate(
        avg_rating=Avg('reviews__rating', distinct=True),
        reviews_count=Count('reviews', distinct=True),
    ).order_by('start_at')
    return render(request, 'organizers/organizer_detail.html', {'organizer': organizer, 'events': events})
