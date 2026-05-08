from warrant_form.code_handler import ThaiCountryAreaCode, CountryNationalityCode, CourtCodeList
import datetime
from django import forms
from django.utils import timezone

CURRENT_TIMEZONE = timezone.get_current_timezone()

today_year = datetime.date.today().year
year_choices = [(year, year + 543) for year in range(1970, today_year + 1)]

year_choices_extended = [(year, year + 543) for year in range(1970, today_year + 50)]

day_choices = [(day, day) for day in range(1, 31 + 1)]
month_choices = [
    (1, "มกราคม"),
    (2, "กุมภาพันธ์"),
    (3, "มีนาคม"),
    (4, "เมษายน"),
    (5, "พฤษภาคม"),
    (6, "มิถุนายน"),
    (7, "กรกฎาคม"),
    (8, "สิงหาคม"),
    (9, "กันยายน"),
    (10, "ตุลาคม"),
    (11, "พฤศจิกายน"),
    (12, "ธันวาคม"),
]

THAI_MONTHS = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10:"ตุลาคม",
    11:"พฤศจิกายน",
    12:"มกราคม",
}

thai_codes = ThaiCountryAreaCode()

nation_codes = CountryNationalityCode()

court_codes = CourtCodeList()

from admin_panel.models import SelectedCourt

court_codes_choices = [
    (court.data.get("court_code"), court.data.get("name")) 
    for court in SelectedCourt.objects.all()
]

if not court_codes_choices:
    court_codes_choices = [("-1" ,"ไม่มีศาลให้เลือก กรุณาติดต่อผู้ดูแลระบบ")]

def reattachDateTime(current_dict : dict, field : str):
        
    scene_date_year = current_dict.get(f"{field}_year")
    scene_date_month = current_dict.get(f"{field}_month")
    scene_date_day = current_dict.get(f"{field}_day")
    scene_date_timehalf = current_dict.get(f"{field}_timehalf")
    combined_date = ""
    combined_datetime = "1970-01-01T00:00:00Z"
    if scene_date_year and scene_date_month and scene_date_day:
        converted_year = scene_date_year 
        padded_month = str(scene_date_month).zfill(2)
        padded_day = str(scene_date_day).zfill(2)

        combined_date = f"{converted_year}-{padded_month}-{padded_day}"

    if combined_date and scene_date_timehalf:
        combined_datetime = f"{combined_date}T{scene_date_timehalf}"

    current_dict.pop(f"{field}_year", None)
    current_dict.pop(f"{field}_month", None)
    current_dict.pop(f"{field}_day", None)
    current_dict.pop(f"{field}_timehalf", None)

    current_dict.update({f"{field}": combined_datetime})

    return current_dict

def createDupe(duped_list : list[str], target_dict : dict) -> dict[str,]:
    for item in duped_list:
        target_dict.update({f"{item}_1" : target_dict.get(item)})
        target_dict.update({f"{item}_2" : target_dict.get(item)})

    return target_dict

def splitTime(time_split_list : list[str], target_dict : dict, month_as_text : bool = False, two_digit_year : bool = False, buddhist_year : bool = False) -> dict[str,]:
    for item in time_split_list:
        datetime_obj : datetime.datetime = target_dict.get(item)

        if datetime_obj:
            datetime_obj = datetime_obj.astimezone(CURRENT_TIMEZONE)

            target_dict.update({f"{item}_day" : datetime_obj.day})

            if month_as_text:
                target_dict.update({f"{item}_month" : THAI_MONTHS.get(datetime_obj.month)})
            else:
                target_dict.update({f"{item}_month" : datetime_obj.month})

            if buddhist_year:
                current_year = datetime_obj.year + 543
            else:
                current_year = datetime_obj.year

            if two_digit_year:
                target_dict.update({f"{item}_year" : int(str(current_year)[-2:])})
            else:
                target_dict.update({f"{item}_year" : current_year})

            target_dict.update({f"{item}_timehalf" : datetime_obj.time().isoformat()})
        else:
            target_dict.update({f"{item}_day" : 1})

            if month_as_text:
                target_dict.update({f"{item}_month" : THAI_MONTHS.get(1)})
            else:
                target_dict.update({f"{item}_month" : 1})

            if two_digit_year:
                target_dict.update({f"{item}_year" : 70})
            else:
                target_dict.update({f"{item}_year" : 1970})

            target_dict.update({f"{item}_timehalf" : "07:00:00"})

    return target_dict