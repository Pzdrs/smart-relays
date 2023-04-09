function toggleRelay(relayId) {
    const currentState = document.querySelector(`#relaySwitch${relayId}`).checked;
    fetch(`/api/relay/${relayId}/toggle/`, {
        method: 'POST',
        headers: {'X-CSRFToken': document.getElementById('csrf_token').innerText}
    }).then(() => changeRelayState(relayId, currentState));
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