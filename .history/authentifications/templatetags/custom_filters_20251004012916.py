from django import template

register = template.Library()

@register.filter
def example_filter(value):
    return value.upper()  # exemple simple
