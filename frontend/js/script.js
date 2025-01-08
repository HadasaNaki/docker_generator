const form = document.getElementById('dockerForm');
const messageDiv = document.getElementById('message');
const base_backend_url = `${window.location.protocol}//${window.location.hostname}:8000`

form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const messageDiv = document.getElementById('message');

    const fileInput = formData.get('file');
    if (!fileInput || !fileInput.size) {
        formData.delete('file');
    }

    try {
        messageDiv.style.display = 'block';
        messageDiv.className = 'message';
        messageDiv.textContent = 'Creating container...';

        const response = await fetch(`${base_backend_url}/create-container`, {
            method: 'POST', body: formData
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.className = 'message success';
            messageDiv.textContent = `Success: ${data.message}`;
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = `Error: ${data.detail || 'Unknown error'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.className = 'message error';
        messageDiv.textContent = 'Error: Unable to login';
    }
});