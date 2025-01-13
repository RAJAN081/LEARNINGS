const display = document.getElementById('display');

// Append input to the display
function appendInput(value) {
    display.value += value;
}

// Clear the display
function clearDisplay() {
    display.value = '';
}

// Send input to the backend for calculation
async function calculate() {
    const expression = display.value;
    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression })
        });
        const data = await response.json();
        display.value = data.result;
    } catch (error) {
        display.value = 'Error';
    }
}

// Keyboard input support
document.addEventListener('keydown', (event) => {
    if ((event.key >= '0' && event.key <= '9') || ['+', '-', '*', '/', '.', '(', ')'].includes(event.key)) {
        appendInput(event.key);
    } else if (event.key === 'Enter') {
        calculate();
    } else if (event.key === 'Backspace') {
        display.value = display.value.slice(0, -1);
    } else if (event.key === 'Escape') {
        clearDisplay();
    }
});
