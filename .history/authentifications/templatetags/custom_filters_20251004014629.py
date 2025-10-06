from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à une clé de dictionnaire avec une variable."""
    return dictionary.get(key)