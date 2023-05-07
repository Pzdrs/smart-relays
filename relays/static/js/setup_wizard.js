const wizard_data = JSON.parse(document.querySelector('#wizard_data').innerText);
const wizard_steps = document.querySelectorAll('.step-item');

Array.from(wizard_steps).slice(0, wizard_data.step + 1).forEach((step) => {
    step.classList.add('is-active');
})

document.querySelectorAll('.wizard-step-input').forEach((input) => {
    input.value = wizard_data.step;
});

if (wizard_data.completed) {
    setTimeout(() => {
        window.location.replace(window.location.origin);
    }, 5000);
} else if (wizard_data.step === 1) {
    addGPIOPinForm(true);
}


function onPasswordFieldChange() {
    const password = document.querySelector('input[name=password1]');
    const confirm = document.querySelector('input[name=password2]');
    if (confirm.value === password.value) {
        confirm.setCustomValidity('');
    } else {
        confirm.setCustomValidity('Passwords do not match');
    }
    confirm.reportValidity();
}

function addGPIOPinForm(first = false) {
    const form_container = document.querySelector('#gpio-pins');
    const form_template = document.querySelector('#add-gpio-pin-form');

    const form = form_template.content.cloneNode(true);

    const delete_button = form.querySelector('.is-danger');
    if (first) delete_button.parentElement.remove();

    form_container.appendChild(form);
}

function testChannel(button) {
    const input = button.parentElement.previousElementSibling.querySelector('input');
    if (input.value === '') {
        input.setCustomValidity('Please fill out this field.');
        input.reportValidity();
        return;
    }

    fetch(`${button.dataset['href']}?pin=${input.value}`)
        .then(_ => {
        });
}

function onSubmit(form) {
    const pinsInput = document.querySelector('input[name=pins]');
    const pinInputs = document.querySelectorAll('input[type=number]');
    pinsInput.value = JSON.stringify(Array.from(pinInputs).map(input => input.value));
    console.log(pinsInput.value);
    return true;
}