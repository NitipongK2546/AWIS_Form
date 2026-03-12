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

    changeSelectValue("10", req_district_sel, all_district)
    changeSelectValue("10", acc_district_sel, all_district)

    changeSelectValue("1001", req_sub_district_sel, all_sub_district)
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
