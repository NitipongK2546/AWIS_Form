// Variable setup
const warrant_form = document.getElementById("warrant-form");

warrant_form.addEventListener("submit", function () {
    is_submitting_form = true;
});
window.addEventListener("beforeunload", function (e) {
    if (!is_submitting_form) {
        e.preventDefault();
    }
});
