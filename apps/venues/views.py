from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import OrganizerRequiredMixin
from apps.venues.forms import VenueForm
from apps.venues.models import Venue


class VenueCreateView(OrganizerRequiredMixin, CreateView):
    model = Venue
    form_class = VenueForm
    template_name = 'venues/venue_form.html'
    success_url = reverse_lazy('venues:list')

    def form_valid(self, form):
        messages.success(self.request, _('Площадка создана.'))
        return super().form_valid(form)


class VenueUpdateView(OrganizerRequiredMixin, UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = 'venues/venue_form.html'
    success_url = reverse_lazy('venues:list')

    def form_valid(self, form):
        messages.success(self.request, _('Площадка обновлена.'))
        return super().form_valid(form)


class VenueDeleteView(OrganizerRequiredMixin, DeleteView):
    model = Venue
    template_name = 'venues/venue_confirm_delete.html'
    success_url = reverse_lazy('venues:list')


def venue_list(request):
    venues = Venue.objects.select_related('city').all()
    paginator = Paginator(venues, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'venues/venue_list.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode()},
    )


def venue_detail(request, slug):
    venue = get_object_or_404(Venue.objects.select_related('city'), slug=slug)
    events = venue.events.annotate(
        avg_rating=Avg('reviews__rating', distinct=True),
        reviews_count=Count('reviews', distinct=True),
    ).order_by('start_at')
    return render(request, 'venues/venue_detail.html', {'venue': venue, 'events': events})
