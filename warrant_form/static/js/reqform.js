
// Variable setup
const awis_form = document.getElementById("awis-form");

const year_selector = document.getElementById("id_main_form-scene_date_year");
const month_selector = document.getElementById("id_main_form-scene_date_month");
const day_selector = document.getElementById("id_main_form-scene_date_day");

let req_province_sel = document.getElementById("id_main_form-req_province");
let req_district_sel = document.getElementById("id_main_form-req_district");
let req_sub_district_sel = document.getElementById("id_main_form-req_sub_district");

let acc_province_sel = document.getElementById("id_main_form-acc_province");
let acc_district_sel = document.getElementById("id_main_form-acc_district");
let acc_sub_district_sel = document.getElementById("id_main_form-acc_sub_district");

let is_submitting_form = false;

let all_district = [];
let all_sub_district = [];

// Setup Code
for (let element of req_district_sel) {
    all_district.push({
        "value": element.value,
        "innerText": element.innerText,
    })
}
for (let element of req_sub_district_sel) {
    all_sub_district.push({
        "value": element.value,
        "innerText": element.innerText,
    })
}

// Non-Async Function
function adjustYearToLatest() {
    year_selector.value = new Date().getFullYear();
}
function changeSelectValue(frontal_substring, targeted_sel, full_list) {
    let options = [];
    for (let child of full_list) {
        if (String(child.value).startsWith(frontal_substring)) {
            options.push(child);
        }
    }
    targeted_sel.innerHTML = "";
    options.forEach(dict => {
        let optionElement = document.createElement("option");
        optionElement.value = dict.value;
        optionElement.innerText = dict.innerText;

        targeted_sel.appendChild(optionElement);
    });
}

// AUTORUN ON START
adjustYearToLatest();
changeSelectValue("10", req_district_sel, all_district)
changeSelectValue("10", acc_district_sel, all_district)

// EVENT LISTENERS
code_select_arr = [
    [req_province_sel, req_district_sel, req_sub_district_sel,],
    [acc_province_sel, acc_district_sel, acc_sub_district_sel,],
]
code_select_arr.forEach(element => {
    // FOR PROVINCE TO CHANGE DISTRICT
    element[0].addEventListener("change", function () {
        changeSelectValue(element[0].value, element[1], all_district);
        changeSelectValue(element[1].value, element[2], all_sub_district);
    });
    // FOR DISTRICT TO CHANGE SUB_DISTRICT
    element[1].addEventListener("change", function () {
        changeSelectValue(element[1].value, element[2], all_sub_district);
    });
});
awis_form.addEventListener("submit", function () {
    is_submitting_form = true;
});
window.addEventListener("beforeunload", function (e) {
    if (!is_submitting_form) {
        e.preventDefault();
    }
});
