from django import template
import datetime
from django.utils import timezone

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
def buddhist_date(value : datetime.datetime | str, select_val : str = None):
    if not value:
        return ""
    
    if isinstance(value, str):
        return value
    
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        aware_time = timezone.make_aware(value)
    else:
        aware_time = timezone.localtime(value)
    
    if not select_val:
        return f"{aware_time.strftime("%d")} {THAI_MONTHS.get(aware_time.month)[1]} {str(aware_time.year + 543)}, {aware_time.strftime("%H:%M")} น."
    
    match select_val:
        case "j":
            return f"{aware_time.strftime("%d")}"
        case "F":
            return f"{THAI_MONTHS.get(aware_time.month)[1]}"
        case "Y":
            return f"{str(aware_time.year + 543)}"
        case "T":
            return f"{aware_time.strftime("%H:%M")} น."