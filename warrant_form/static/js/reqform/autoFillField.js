const accused_1 = document.getElementById("id_main_form-accused_1");
const accused_2 = document.getElementById("id_main_form-accused_2");

const plaintiff_1 = document.getElementById("id_main_form-plaintiff_1");
const plaintiff_2 = document.getElementById("id_main_form-plaintiff_2");

const court_name_1 = document.getElementById("id_main_form-court_name_1");
const court_name_2 = document.getElementById("id_main_form-court_name_2");

accused_1.addEventListener("input", () => {
    accused_2.value = accused_1.value;
});

accused_2.addEventListener("input", () => {
    accused_1.value = accused_2.value;
});

plaintiff_1.addEventListener("input", () => {
    plaintiff_2.value = plaintiff_1.value;
});

plaintiff_2.addEventListener("input", () => {
    plaintiff_1.value = plaintiff_2.value;
});

court_name_1.addEventListener("input", () => {
    court_name_2.value = court_name_1.value;
});

court_name_2.addEventListener("input", () => {
    court_name_1.value = court_name_2.value;
});
