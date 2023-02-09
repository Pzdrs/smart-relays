// on page load
document.addEventListener('DOMContentLoaded', function () {
    const relays = JSON.parse(document.querySelector('#relays').innerText);
    for (const [id, state] of Object.entries(relays)) {
        changeRelayState(id, state);
    }
});

function toggleRelay(relayId) {
    const currentState = document.querySelector(`#relaySwitch${relayId}`).checked;
    changeRelayState(relayId, currentState);
}

function changeRelayState(relayId, state) {
    const cardHeader = document.querySelector(`#relayCardHeader${relayId}`);
    const relaySwitch = document.querySelector(`#relaySwitch${relayId}`)
    relaySwitch.checked = state;
    if (state) {
        cardHeader.classList.remove('has-background-danger-light');
        cardHeader.classList.add('has-background-success-light');
    } else {
        cardHeader.classList.remove('has-background-success-light');
        cardHeader.classList.add('has-background-danger-light');
    }
}