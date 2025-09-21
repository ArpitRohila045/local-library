from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    """Gets a dictionary value by key in Django template."""
    if d and key in d:
        return d.get(key)
    return None