from django import template

register = template.Library()


@register.filter
def pesos_chilenos(precio):
    return f'${precio:,}'.replace(',', '.')
