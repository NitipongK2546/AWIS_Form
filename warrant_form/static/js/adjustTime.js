function adjustTimeToLatest() {

    let hours = current_date.getHours();
    let mins = current_date.getMinutes();

    scene_timehalf_selector.value = hours + ":" + mins
    woa_start_timehalf.value = hours + ":" + mins
    woa_end_timehalf.value = hours + ":" + mins
}
adjustTimeToLatest();