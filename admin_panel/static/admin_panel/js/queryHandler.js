// const timelogged = document.getElementById("timelogged-trigger");
// const user = document.getElementById("user-trigger");
// const action = document.getElementById("action-trigger");
// const reqno = document.getElementById("reqno-trigger");

const collections = ["timelogged", "user", "action", "reqno"]

collections.forEach(element => {
    let trigger = document.getElementById(`id_${element}_trigger`);
    let container = document.getElementById(`${element}-container`);
    let inputs = container.querySelectorAll('input, select');

    function updateState() {
        if (trigger.checked) {
            inputs.forEach(input => input.disabled = false);
            container.classList.remove("hidden");
        } else {
            inputs.forEach(input => input.disabled = true);
            container.classList.add("hidden");
        }
    }

    updateState();

    trigger.addEventListener('change', () => {
        updateState()
    });
});

// function disableQueryInput() {
    
// }
