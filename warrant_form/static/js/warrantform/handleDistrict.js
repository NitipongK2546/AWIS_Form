let acc_province_sel = document.getElementById("id_acc_province");
let acc_district_sel = document.getElementById("id_acc_district");
let acc_sub_district_sel = document.getElementById("id_acc_sub_district");

let is_submitting_form = false;

let all_district = [];
let all_sub_district = [];

// NEW Setup Code
const csrftoken = getCookie("csrftoken")

async function fetchSelectItems(target_url) {
    const response = await fetch(target_url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })

    const data = await response.json();
    
    return data["data"]
}

async function setUpArray() {
    all_district_array = await fetchSelectItems('/api/internal/get-district/')
    all_sub_district_array = await fetchSelectItems('/api/internal/get-sub-district/')

    for (let element of all_district_array) {
    all_district.push({
        "value": element[0],
        "innerText": element[1],
    })
    }
    for (let element of all_sub_district_array) {
        all_sub_district.push({
            "value": element[0],
            "innerText": element[1],
        })
    }

    changeSelectValue("10", acc_district_sel, all_district)
    changeSelectValue("1001", acc_sub_district_sel, all_sub_district)
}

// Non-Async Function

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