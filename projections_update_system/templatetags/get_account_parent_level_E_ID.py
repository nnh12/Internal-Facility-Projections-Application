from django.template.defaulttags import register

@register.filter
def get_account_parent_level_E_ID(key):
    return key.split("~")[0]