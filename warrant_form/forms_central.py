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
    combined_datetime = "1970-01-01 00:00:00"
    if scene_date_year and scene_date_month and scene_date_day:
        converted_year = scene_date_year 
        padded_month = str(scene_date_month).zfill(2)
        padded_day = str(scene_date_day).zfill(2)

        combined_date = f"{converted_year}-{padded_month}-{padded_day}"

    if combined_date and scene_date_timehalf:
        combined_datetime = f"{combined_date} {scene_date_timehalf}"

    current_dict.pop(f"{field}_year", None)
    current_dict.pop(f"{field}_month", None)
    current_dict.pop(f"{field}_day", None)
    current_dict.pop(f"{field}_timehalf", None)

    current_dict.update({f"{field}": combined_datetime})

    return current_dict