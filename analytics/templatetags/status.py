from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.assignment_tag
def status_get(status):
    status_dct = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}
    return status_dct[status]
