acc_full_name_1.addEventListener("input", () => {
    acc_full_name_2.value = acc_full_name_1.value;
});

acc_full_name_2.addEventListener("input", () => {
    acc_full_name_1.value = acc_full_name_2.value;
});