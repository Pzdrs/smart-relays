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