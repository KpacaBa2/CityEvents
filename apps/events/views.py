from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import OrganizerMemberRequiredMixin, OrganizerRequiredMixin
from apps.events.forms import EventForm
from apps.events.models import Event
from apps.organizers.models import OrganizerMember


class EventCreateView(OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        messages.success(self.request, _('Событие создано.'))
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            allowed_ids = OrganizerMember.objects.filter(user=user).values_list('organizer_id', flat=True)
            form.fields['organizer'].queryset = form.fields['organizer'].queryset.filter(id__in=allowed_ids)
        return form

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'slug': self.object.slug})


class EventUpdateView(OrganizerMemberRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        messages.success(self.request, _('Событие обновлено.'))
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            allowed_ids = OrganizerMember.objects.filter(user=user).values_list('organizer_id', flat=True)
            form.fields['organizer'].queryset = form.fields['organizer'].queryset.filter(id__in=allowed_ids)
        return form

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'slug': self.object.slug})


class EventDeleteView(OrganizerMemberRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:list')



def event_list(request):
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

    paginator = Paginator(events.distinct(), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'events/event_list.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode()},
    )


def event_detail(request, slug):
    event = get_object_or_404(
        Event.objects.select_related('venue', 'organizer')
        .prefetch_related('categories', 'tags', 'images', 'reviews')
        .annotate(
            avg_rating=Avg('reviews__rating', distinct=True),
            reviews_count=Count('reviews', distinct=True),
        ),
        slug=slug,
    )
    can_manage = False
    user = request.user
    if user.is_authenticated:
        if user.is_staff or user.is_superuser:
            can_manage = True
        else:
            profile = getattr(user, 'userprofile', None)
            if profile and profile.role in {'organizer', 'staff'}:
                can_manage = OrganizerMember.objects.filter(
                    user=user,
                    organizer=event.organizer,
                ).exists()
    return render(request, 'events/event_detail.html', {'event': event, 'can_manage': can_manage})


@login_required
def my_events(request):
    events = (
        Event.objects.select_related('venue', 'organizer')
        .prefetch_related('categories', 'tags')
        .annotate(
            avg_rating=Avg('reviews__rating', distinct=True),
            reviews_count=Count('reviews', distinct=True),
        )
    )

    user = request.user
    has_access = True
    if not (user.is_staff or user.is_superuser):
        profile = getattr(user, 'userprofile', None)
        if not profile or profile.role not in {'organizer', 'staff'}:
            events = events.none()
            has_access = False
        else:
            allowed_ids = OrganizerMember.objects.filter(user=user).values_list('organizer_id', flat=True)
            events = events.filter(organizer_id__in=allowed_ids)

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

    paginator = Paginator(events.distinct(), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'events/my_events.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode(), 'has_access': has_access},
    )
