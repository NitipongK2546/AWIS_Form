function adjustDateToLatest() {
    let current_year = current_date.getFullYear();

    woa_date_year.value = current_year;
}

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

function changeDate(day_element, month_element) {
    day_element.innerHTML = ""
    if (month_element.value == 2) {
        createDayOption(28, day_element)
    }
    else if ([4,6,9,11].includes(Number(month_element.value))) {
        createDayOption(30, day_element)
    }
    else{
        createDayOption(31, day_element)
    }
}

adjustDateToLatest();