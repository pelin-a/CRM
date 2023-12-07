from django import template

register = template.Library()

@register.filter
def get_stage(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    else:
        return ''