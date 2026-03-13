const cause_type_id_1 = document.getElementById("id_main_form-cause_type_id_1");
const cause_type_id_2 = document.getElementById("id_main_form-cause_type_id_2");
const cause_text_1 = document.getElementById("id_main_form-cause_text_1");
const cause_text_2 = document.getElementById("id_main_form-cause_text_2");

const have_req_1 = document.getElementById("id_main_form-have_req_1");
const have_req_2 = document.getElementById("id_main_form-have_req_2");

cause_type_id_1.addEventListener("change", () => {
    if (cause_type_id_1.checked) {
        cause_type_id_2.disabled = true
        cause_text_2.disabled = true
    }
    else {
        cause_type_id_2.disabled = false
        cause_text_2.disabled = false
    }
});

cause_type_id_2.addEventListener("change", () => {
    if (cause_type_id_2.checked) {
        cause_type_id_1.disabled = true
        cause_text_1.disabled = true
    }
    else {
        cause_type_id_1.disabled = false
        cause_text_1.disabled = false
    }
});

have_req_1.addEventListener("change", () => {
    if (have_req_1.checked) {
        have_req_2.disabled = true
    }
    else {
        have_req_2.disabled = false
    }
});

have_req_2.addEventListener("change", () => {
    if (have_req_2.checked) {
        have_req_1.disabled = true
    }
    else {
        have_req_1.disabled = false
    }
});