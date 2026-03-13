// Variable setup
const awis_form = document.getElementById("awis-form");

awis_form.addEventListener("submit", function () {
    is_submitting_form = true;
});
window.addEventListener("beforeunload", function (e) {
    if (!is_submitting_form) {
        e.preventDefault();
    }
});