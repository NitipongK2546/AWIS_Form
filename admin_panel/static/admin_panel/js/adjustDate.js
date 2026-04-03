const current_date = new Date()

const req_day = document.getElementById("id_end_day");
const req_month = document.getElementById("id_end_month");
const req_year = document.getElementById("id_end_year");

function adjustDateToLatest() {
    // let current_year = current_date.getFullYear();

    req_year.value = current_date.getFullYear();
    req_month.value = current_date.getMonth() + 1;
    req_day.value = current_date.getDate();
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

adjustDateToLatest();