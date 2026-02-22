from django.core.paginator import Paginator
from django.shortcuts import render

from apps.tags.models import Tag


def tag_list(request):
    tags = Tag.objects.all()
    paginator = Paginator(tags, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    querystring = request.GET.copy()
    querystring.pop('page', None)
    return render(
        request,
        'tags/tag_list.html',
        {'page_obj': page_obj, 'querystring': querystring.urlencode()},
    )
