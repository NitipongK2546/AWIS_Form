let warrant_acc_province_sel = document.getElementById("id_acc_province");
let warrant_acc_district_sel = document.getElementById("id_acc_district");
let warrant_acc_sub_district_sel = document.getElementById("id_acc_sub_district");

async function setUpArray() {
    await fetchDistrictDataFromServer()

    changeSelectValue(acc_province, warrant_acc_district_sel, all_district)
    changeSelectValue(acc_district, warrant_acc_sub_district_sel, all_sub_district)

    warrant_acc_province_sel.value = acc_province
    warrant_acc_district_sel.value = acc_district
    warrant_acc_sub_district_sel.value = acc_sub_district
}

// AUTORUN ON START

setUpArray()

// EVENT LISTENERS
code_select_arr = [
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