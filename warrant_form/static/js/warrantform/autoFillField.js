const send_to_name = document.getElementById("id_send_to_name");
const acc_full_name_1 = document.getElementById("id_acc_full_name_1");
const acc_full_name_2 = document.getElementById("id_acc_full_name_2");

acc_full_name_1.addEventListener("input", () => {
    acc_full_name_2.value = acc_full_name_1.value;
});

acc_full_name_2.addEventListener("input", () => {
    acc_full_name_1.value = acc_full_name_2.value;
});