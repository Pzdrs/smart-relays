function toggleRelay(checkbox, relayId) {
    checkbox.disabled = true;
    const currentState = checkbox.checked;
    fetch(`/relays/${relayId}/toggle/`, {
        method: 'POST',
        headers: {'X-CSRFToken': document.getElementById('csrf_token').innerText}
    }).then(() => changeRelayState(relayId, currentState));
}

function changeRelayState(relayId, state) {
    const cardHeader = document.querySelector(`#relayCardHeader${relayId}`);
    const relaySwitch = document.querySelector(`#relaySwitch${relayId}`)
    const history = document.querySelector(`#relayHistory_${relayId}`);
    history.innerHTML = 'Right now';
    relaySwitch.checked = state;
    if (state) {
        cardHeader.classList.remove('has-background-danger-light');
        cardHeader.classList.add('has-background-success-light');
    } else {
        cardHeader.classList.remove('has-background-success-light');
        cardHeader.classList.add('has-background-danger-light');
    }
    setTimeout(() => relaySwitch.disabled = false, 200);
}