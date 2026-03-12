from django import template
import datetime

register = template.Library()

@register.filter(name="buddhist_date")
def buddhist_date(value : datetime.datetime):
    if not value:
        return ""
    return value.strftime("%d/%m/") + str(value.year + 543) + value.strftime("%H:%M น.")