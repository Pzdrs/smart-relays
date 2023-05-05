function getStateLabel(state) {
    if (state === 0) {
        return 'OFF';
    } else if (state === 1) {
        return 'ON';
    } else {
        return '';
    }
}

const data = JSON.parse(document.getElementById('state_history').textContent);
new Chart(document.getElementById('history'), {
    type: 'line',
    options: {
        scales: {
            x: {
                type: 'time',
                grid: {
                    display: false
                }
            },
            y: {
                ticks: {
                    callback: value => getStateLabel(value)
                }
            }
        }
    },
    data: {
        labels: Object.keys(data),
        datasets: [
            {
                label: 'Relay state',
                data: Object.values(data),
                stepped: true
            }
        ],
    }
});