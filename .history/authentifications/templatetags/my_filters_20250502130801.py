from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
from django import template

register = template.Library()

@register.filter
def upper(value):
    return value.upper()
