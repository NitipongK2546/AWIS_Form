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

function newCheckbox(isChecked = false) {
    const elem = document.createElement("span");
    elem.className = "checkbox-display";

    if (isChecked) {
        elem.textContent = "✓"
        elem.classList.add("checked");
    }
    else {
        elem.classList.add("unchecked");
    }

    return elem
}

checkbox_inputs.forEach(element => {
    if (element.checked) {
        element.replaceWith(
            newCheckbox(true)
        )
    }
    else {
        element.replaceWith(
            newCheckbox()
        )
    }
});