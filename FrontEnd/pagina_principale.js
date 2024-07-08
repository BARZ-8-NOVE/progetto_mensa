document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('jwt');

    // Controlla se il token è presente per verificare se l'utente è loggato
    if (!token) {
        // Se il token non è presente, reindirizza alla pagina di login
        window.location.href = 'login.html';
        return;
    }

    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('username').textContent = username;
    }

    document.getElementById('logout').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/utenti/do_logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                // Rimuove il token e le informazioni utente da localStorage
                localStorage.removeItem('jwt');
                localStorage.removeItem('username');
                // Redirige alla pagina di login
                window.location.href = 'login.html';
            } else {
                throw new Error('Logout fallito');
            }
        })
        .catch(error => {
            console.error('Errore durante il logout:', error);
            alert('Si è verificato un errore durante il logout');
        });
    });
});