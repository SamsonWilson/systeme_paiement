# templatetags/filters.py
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Renvoie l'élément d'un dictionnaire basé sur la clé."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
