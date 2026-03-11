// Variable setup
const awis_form = document.getElementById("awis-form");
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

let req_province_sel = document.getElementById("id_main_form-req_province");
let req_district_sel = document.getElementById("id_main_form-req_district");
let req_sub_district_sel = document.getElementById("id_main_form-req_sub_district");

let acc_province_sel = document.getElementById("id_main_form-acc_province");
let acc_district_sel = document.getElementById("id_main_form-acc_district");
let acc_sub_district_sel = document.getElementById("id_main_form-acc_sub_district");

const accused_1 = document.getElementById("id_main_form-accused_1");
const accused_2 = document.getElementById("id_main_form-accused_2");

const plaintiff_1 = document.getElementById("id_main_form-plaintiff_1");
const plaintiff_2 = document.getElementById("id_main_form-plaintiff_2");

const court_name_1 = document.getElementById("id_main_form-court_name_1");
const court_name_2 = document.getElementById("id_main_form-court_name_2");