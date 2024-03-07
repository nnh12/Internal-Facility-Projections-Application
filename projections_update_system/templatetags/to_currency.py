from django.template.defaulttags import register

@register.filter
def to_currency(rawFloat):
    value = '{0:,.0f}'.format(abs(float(rawFloat)))
    if rawFloat < 0:
        return '(' + value + ')'
    return value