from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter

def index(List, i):
    return List[int(i)]
