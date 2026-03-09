function adjustDateToLatest() {
    let current_year = current_date.getFullYear();

    req_year.value = current_date.getFullYear();
    req_month.value = current_date.getMonth() + 1;
    req_day.value = current_date.getDate();

    scene_year_selector.value = current_year;
    woa_start_year.value = current_year;
    woa_end_year.value = current_year;

}
adjustDateToLatest();