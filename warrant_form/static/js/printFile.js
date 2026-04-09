const print_button = document.getElementById("print-doc")
const time_inputs = document.querySelectorAll('input[type="time"]')
const checkbox_inputs = document.querySelectorAll('input[type="checkbox"]')

////////////////////////////////////////////////////////////////

function printPage() {
    window.print();
}

print_button.addEventListener("click", () => {
    printPage()
})

///////////////////////////////////////////////////////////////

time_inputs.forEach(element => {
    element.removeAttribute("type")
});

