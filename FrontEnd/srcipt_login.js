document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene il comportamento predefinito del form

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/utenti/do_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Errore durante il login');
        }
        return response.json();
    })
    .then(data => {
        if (data.token) {
            // Salva il token JWT in localStorage
            localStorage.setItem('jwt', data.token);
            localStorage.setItem('username', data.username);
            // Reindirizza alla pagina principale
            window.location.href = 'pagina_principale.html'; 
        } else {
            // Gestione degli errori
            alert('Errore di login: ' + (data.message || 'Credenziali non valide'));
        }
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante il login');
    });
});
