from django import template

register = template.Library()


@register.filter
def stars(value: int) -> str:
    try:
        rating = int(value)
    except (TypeError, ValueError):
        rating = 0
    rating = max(0, min(rating, 5))
    return '*' * rating + '-' * (5 - rating)


@register.simple_tag(takes_context=True)
def active_class(context, pattern: str) -> str:
    request = context.get('request')
    if not request:
        return ''
    path = request.path
    if pattern == '/':
        return 'is-active' if path == '/' else ''
    return 'is-active' if path.startswith(pattern) else ''
