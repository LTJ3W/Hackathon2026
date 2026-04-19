function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
}

function addMessage(text, className) {
    const box = document.getElementById('chat-box');
    if (!box) return;

    const msg = document.createElement('div');
    msg.className = `chat-message ${className}`;
    msg.textContent = text;
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('chat-input');

    if (!form || !input || !window.fitGuideChatUrl) return;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const message = input.value.trim();
        if (!message) return;

        addMessage(message, 'user-message');
        input.value = '';

        try {
            const response = await fetch(window.fitGuideChatUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            addMessage(data.reply || data.error || 'No response received.', 'bot-message');
        } catch (error) {
            addMessage('Sorry, something went wrong.', 'bot-message');
        }
    });
});