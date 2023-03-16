from django import template


register = template.Library()


@register.filter()
def date_converter(date):
    new_date = date.strftime("%d.%m.%Y %H:%M:%S")
    return f'{new_date}'

