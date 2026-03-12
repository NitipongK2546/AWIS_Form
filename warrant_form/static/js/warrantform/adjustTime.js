function adjustTimeToLatest() {

    let hours = current_date.getHours();
    let mins = current_date.getMinutes();

    woa_date_timehalf.value = hours + ":" + mins
}
adjustTimeToLatest();