from django import template

register = template.Library()

@register.filter
def replace_dot_with_comma(value):
    return str(value).replace('.', ',')