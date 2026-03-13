const current_date = new Date()

const woa_date_year = document.getElementById("id_woa_date_year");
const woa_date_month = document.getElementById("id_woa_date_month");
const woa_date_day = document.getElementById("id_woa_date_day");
const woa_date_timehalf = document.getElementById("id_woa_date_timehalf");

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