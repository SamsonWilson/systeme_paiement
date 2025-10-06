from django import template
register = template.Library()

@register.filter
def upper_case(value):
    return value.upper()
