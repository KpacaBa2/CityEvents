from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from apps.categories.forms import CategoryForm
from apps.categories.models import Category
from apps.core.mixins import OrganizerRequiredMixin
from apps.events.models import Event


class CategoryCreateView(OrganizerRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        messages.success(self.request, _('Категория создана.'))
        return super().form_valid(form)


class CategoryUpdateView(OrganizerRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        messages.success(self.request, _('Категория обновлена.'))
        return super().form_valid(form)


class CategoryDeleteView(OrganizerRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:list')


def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'categories/category_list.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode()},
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    events = (
        Event.objects.filter(categories=category)
        .annotate(
            avg_rating=Avg('reviews__rating', distinct=True),
            reviews_count=Count('reviews', distinct=True),
        )
        .order_by('start_at')
    )
    return render(request, 'categories/category_detail.html', {'category': category, 'events': events})
