const current_date = new Date()

const woa_date_year = document.getElementById("id_woa_date_year");
const woa_date_month = document.getElementById("id_woa_date_month");
const woa_date_day = document.getElementById("id_woa_date_day");
const woa_date_timehalf = document.getElementById("id_woa_date_timehalf");

function createDayOption(maxDays, target_element) {

    for (let i = 1; i <= 31; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = i;

        if (i > maxDays) {
            break;
        }

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

function adjustDateToLatest() {
    let current_year = current_date.getFullYear();

    woa_date_year.value = current_year;
}

function adjustTimeToLatest() {

    let hours = current_date.getHours();
    let mins = current_date.getMinutes();

    woa_date_timehalf.value = hours + ":" + mins
}
adjustTimeToLatest();
adjustDateToLatest();