from pathlib import Path

from django import template

register = template.Library()


@register.simple_tag
def file_href(file_field, request=None, absolute=False):
    if not file_field:
        return ''
    try:
        url = file_field.url
    except (AttributeError, ValueError):
        return ''
    if absolute and request is not None:
        return request.build_absolute_uri(url)
    return url


@register.filter
def file_action_label(filename):
    suffix = Path(str(filename or '')).suffix.lower()
    if suffix in {'.jpg', '.jpeg', '.png'}:
        return 'Открыть изображение'
    return 'Скачать файл'
