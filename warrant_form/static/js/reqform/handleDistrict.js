let req_province_sel = document.getElementById("id_main_form-req_province");
let req_district_sel = document.getElementById("id_main_form-req_district");
let req_sub_district_sel = document.getElementById("id_main_form-req_sub_district");

let acc_province_sel = document.getElementById("id_main_form-acc_province");
let acc_district_sel = document.getElementById("id_main_form-acc_district");
let acc_sub_district_sel = document.getElementById("id_main_form-acc_sub_district");

async function setUpArray() {
    await fetchDistrictDataFromServer()
    
    changeSelectValue(acc_province, acc_district_sel, all_district)
    changeSelectValue(req_province, req_district_sel, all_district)
    
    changeSelectValue(acc_district, acc_sub_district_sel, all_sub_district)
    changeSelectValue(req_district, req_sub_district_sel, all_sub_district)

    req_province_sel.value = req_province
    req_district_sel.value = req_district
    req_sub_district_sel.value = req_sub_district

    acc_province_sel.value = acc_province
    acc_district_sel.value = acc_district
    acc_sub_district_sel.value = acc_sub_district
}

// AUTORUN ON START

setUpArray()

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

