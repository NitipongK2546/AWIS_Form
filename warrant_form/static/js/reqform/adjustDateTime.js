const current_date = new Date()

const req_day = document.getElementById("id_main_form-req_day");
const req_month = document.getElementById("id_main_form-req_month");
const req_year = document.getElementById("id_main_form-req_year");

const scene_date_year = document.getElementById("id_main_form-scene_date_year");
const woa_start_date_year = document.getElementById("id_main_form-woa_start_date_year");
const woa_end_date_year = document.getElementById("id_main_form-woa_end_date_year");

const scene_date_month = document.getElementById("id_main_form-scene_date_month");
const woa_start_date_month = document.getElementById("id_main_form-woa_start_date_month");
const woa_end_date_month = document.getElementById("id_main_form-woa_end_date_month");

const scene_date_day = document.getElementById("id_main_form-scene_date_day");
const woa_start_date_day = document.getElementById("id_main_form-woa_start_date_day");
const woa_end_date_day = document.getElementById("id_main_form-woa_end_date_day");

const scene_timehalf_selector = document.getElementById("id_main_form-scene_date_timehalf");
const woa_start_timehalf = document.getElementById("id_main_form-woa_start_date_timehalf");
const woa_end_timehalf = document.getElementById("id_main_form-woa_end_date_timehalf");

function adjustDateToLatest() {
    let current_year = current_date.getFullYear();

    req_year.value = current_date.getFullYear();
    req_month.value = current_date.getMonth() + 1;
    req_day.value = current_date.getDate();

    scene_date_year.value = current_year;
    woa_start_date_year.value = current_year;
    woa_end_date_year.value = current_year;

}

function createDayOption(maxDays, target_element) {

    for (let i = 1; i <= 31; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = i;

        if (i > maxDays) {
            break;
        }

        if (i == 1) { option.selected = true; }

        target_element.appendChild(option);
    }
}

function changeDate(day_element, month_element, year_element) {
    day_element.innerHTML = ""
    if (month_element.value == 2) {

        if (isLeapYear(year_element.value)) {
            createDayOption(29, day_element)
        }
        else {
            createDayOption(28, day_element)
        }
    }
    else if ([4,6,9,11].includes(Number(month_element.value))) {
        createDayOption(30, day_element)
    }
    else{
        createDayOption(31, day_element)
    }
}

function isLeapYear(year) {
    // year = year - 543
    // console.log(year)
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

function adjustTimeToLatest() {

    let hours = current_date.getHours();
    let mins = current_date.getMinutes();

    scene_timehalf_selector.value = hours + ":" + mins + ":00"
    woa_start_timehalf.value = hours + ":" + mins + ":00"
    woa_end_timehalf.value = hours + ":" + mins + ":00"
}

adjustTimeToLatest();
adjustDateToLatest();