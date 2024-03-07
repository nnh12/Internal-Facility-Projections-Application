from django.template.defaulttags import register

@register.filter
def get_value(dictionary, key):
    if not key in dictionary:
        return None
    return dictionary.get(key)