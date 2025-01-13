from django import template

register = template.Library()

@register.simple_tag
def version():
    return '2.2.1'