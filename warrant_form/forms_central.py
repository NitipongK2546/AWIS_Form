from warrant_form.code_handler import ThaiCountryAreaCode
import datetime

today_year = datetime.date.today().year
year_choices = [(year, year + 543) for year in range(1970, today_year + 1)]
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
thai_codes = ThaiCountryAreaCode()

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
        combined_datetime = f"{combined_date}T{scene_date_timehalf}+07:00"

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

def splitTime(time_split_list : list[str], target_dict : dict) -> dict[str,]:
    for item in time_split_list:
        datetime_obj : datetime.datetime = target_dict.get(item)

        target_dict.update({f"{item}_day" : datetime_obj.day})
        target_dict.update({f"{item}_month" : datetime_obj.month})
        target_dict.update({f"{item}_year" : datetime_obj.year})

        target_dict.update({f"{item}_timehalf" : datetime_obj.time().isoformat()})

    return target_dict