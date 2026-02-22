import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from apps.categories.models import Category
from apps.events.models import Event
from apps.organizers.models import OrganizerMember
from apps.reviews.models import Review
from apps.venues.models import Venue


def _error(message: str, code: str = 'bad_request', status: int = 400):
    return JsonResponse({'error': {'code': code, 'message': message}}, status=status)


def _can_manage_event(user, *, organizer_id=None, event: Event | None = None) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    profile = getattr(user, 'userprofile', None)
    if not profile or profile.role not in {'organizer', 'staff'}:
        return False
    if event is not None:
        organizer_id = event.organizer_id
    if organizer_id is None:
        return False
    return OrganizerMember.objects.filter(user=user, organizer_id=organizer_id).exists()


def _event_to_dict(event: Event) -> dict:
    avg_rating = getattr(event, 'avg_rating', None)
    reviews_count = getattr(event, 'reviews_count', None)
    return {
        'id': event.id,
        'title': event.title,
        'slug': event.slug,
        'start_at': event.start_at.isoformat(),
        'end_at': event.end_at.isoformat(),
        'venue': event.venue.name,
        'organizer': event.organizer.name,
        'categories': [c.name for c in event.categories.all()],
        'tags': [t.name for t in event.tags.all()],
        'price_from': str(event.price_from),
        'status': event.status,
        'avg_rating': round(avg_rating, 1) if avg_rating is not None else None,
        'reviews_count': reviews_count if reviews_count is not None else 0,
    }


def _review_to_dict(review: Review) -> dict:
    return {
        'id': review.id,
        'event': review.event.title,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.isoformat(),
    }


def events_collection(request):
    if request.method == 'GET':
        events = (
            Event.objects.select_related('venue', 'organizer')
            .prefetch_related('categories', 'tags')
            .filter(status=Event.STATUS_PUBLISHED)
            .annotate(
                avg_rating=Avg('reviews__rating', distinct=True),
                reviews_count=Count('reviews', distinct=True),
            )
        )
        q = request.GET.get('q')
        if q:
            events = events.filter(Q(title__icontains=q) | Q(organizer__name__icontains=q))
        category = request.GET.get('category')
        if category:
            events = events.filter(categories__slug=category)
        city = request.GET.get('city')
        if city:
            events = events.filter(venue__city__slug=city)
        year = request.GET.get('year')
        if year and year.isdigit():
            events = events.filter(start_at__year=year)
        ordering = request.GET.get('ordering')
        if ordering in {'start_at', '-start_at', 'price_from', '-price_from'}:
            events = events.order_by(ordering)
        paginator = Paginator(events.distinct(), int(request.GET.get('page_size', 10)))
        page = paginator.get_page(request.GET.get('page'))
        data = [_event_to_dict(e) for e in page.object_list]
        return JsonResponse({
            'count': paginator.count,
            'page': page.number,
            'pages': paginator.num_pages,
            'results': data,
        })

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return _error('Invalid JSON payload.', 'invalid_json', 400)

        required = ['title', 'start_at', 'end_at', 'venue_id', 'organizer_id']
        missing = [field for field in required if field not in payload]
        if missing:
            return _error(f"Missing fields: {', '.join(missing)}", 'validation_error', 400)

        if not _can_manage_event(request.user, organizer_id=payload.get('organizer_id')):
            return _error('Not enough permissions.', 'forbidden', 403)

        start_at = parse_datetime(payload['start_at'])
        end_at = parse_datetime(payload['end_at'])
        if not start_at or not end_at:
            return _error('start_at and end_at must be ISO datetime.', 'validation_error', 400)

        event = Event(
            title=payload['title'],
            description=payload.get('description', ''),
            start_at=start_at,
            end_at=end_at,
            venue_id=payload['venue_id'],
            organizer_id=payload['organizer_id'],
            status=payload.get('status', Event.STATUS_DRAFT),
            price_from=payload.get('price_from', 0),
        )
        try:
            event.full_clean()
        except ValidationError as exc:
            return _error('; '.join(exc.messages), 'validation_error', 400)
        event.save()
        return JsonResponse(_event_to_dict(event), status=201)

    return _error('Method not allowed', 'method_not_allowed', 405)


def event_detail(request, slug):
    try:
        event = (
            Event.objects.select_related('venue', 'organizer')
            .prefetch_related('categories', 'tags')
            .annotate(
                avg_rating=Avg('reviews__rating', distinct=True),
                reviews_count=Count('reviews', distinct=True),
            )
            .get(slug=slug)
        )
    except Event.DoesNotExist:
        return _error('Event not found.', 'not_found', 404)

    if request.method == 'GET':
        return JsonResponse(_event_to_dict(event))

    if request.method in {'PUT', 'DELETE'}:
        if not _can_manage_event(request.user, event=event):
            return _error('Not enough permissions.', 'forbidden', 403)

    if request.method == 'DELETE':
        event.delete()
        return JsonResponse({'status': 'deleted'})

    if request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return _error('Invalid JSON payload.', 'invalid_json', 400)
        for field in ['title', 'description', 'status']:
            if field in payload:
                setattr(event, field, payload[field])
        try:
            event.full_clean()
        except ValidationError as exc:
            return _error('; '.join(exc.messages), 'validation_error', 400)
        event.save()
        return JsonResponse(_event_to_dict(event))

    return _error('Method not allowed', 'method_not_allowed', 405)


def categories_list(request):
    data = list(Category.objects.values('id', 'name', 'slug'))
    return JsonResponse({'results': data})


def venues_list(request):
    data = list(Venue.objects.values('id', 'name', 'slug', 'address'))
    return JsonResponse({'results': data})


def reviews_list(request):
    reviews = Review.objects.select_related('event', 'user').order_by('-created_at')
    event_slug = request.GET.get('event')
    if event_slug:
        reviews = reviews.filter(event__slug=event_slug)
    data = [_review_to_dict(r) for r in reviews[:50]]
    return JsonResponse({'results': data})
