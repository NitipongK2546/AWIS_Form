from django import template
import datetime

register = template.Library()

THAI_MONTHS = {
    1: ("ม.ค.", "มกราคม"),
    2: ("ก.พ.", "กุมภาพันธ์"),
    3: ("มี.ค.", "มีนาคม"),
    4: ("เม.ย.", "เมษายน"),
    5: ("พ.ค.", "พฤษภาคม"),
    6: ("มิ.ย.", "มิถุนายน"),
    7: ("ก.ค.", "กรกฎาคม"),
    8: ("ส.ค.", "สิงหาคม"),
    9: ("ก.ย.", "กันยายน"),
    10:("ต.ค.", "ตุลาคม"),
    11:("พ.ย.", "พฤศจิกายน"),
    12:("ธ.ค.", "มกราคม"),
}

@register.filter(name="buddhist_date")
def buddhist_date(value : datetime.datetime):
    if not value:
        return ""
    
    return f"{value.strftime("%d")} {THAI_MONTHS.get(value.month)[1]} {str(value.year + 543)}, {value.strftime("%H:%M")} น."