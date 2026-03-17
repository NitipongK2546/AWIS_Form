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

async function fetchDistrictDataFromServer() {
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
    options.forEach((dict, index) => {
        let optionElement = document.createElement("option");
        optionElement.value = dict.value;
        optionElement.innerText = dict.innerText;

        if (index == 0) { optionElement.selected = true }

        targeted_sel.appendChild(optionElement);
    });
}