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
