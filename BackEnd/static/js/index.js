function showLoadingSpinner() {
    // Mostra uno spinner di caricamento
    const spinnerOverlay = document.createElement('div');
    spinnerOverlay.id = 'globalLoadingOverlay';
    spinnerOverlay.innerHTML = '<div class="spinner"></div>';  // Inserisci qui il tuo spinner
    document.body.appendChild(spinnerOverlay);

    // Rimuovi lo spinner dopo 3 secondi
    setTimeout(() => {
        const spinnerOverlay = document.getElementById('globalLoadingOverlay');
        if (spinnerOverlay) {
            document.body.removeChild(spinnerOverlay);
        }
    }, 1000); // Rimuovi dopo 1 secondo (o qualsiasi valore tu desideri)
}

// Aggiungi un gestore di eventi per tutti i link nel menu
document.querySelectorAll('.load-link').forEach(link => {
    link.addEventListener('click', function(event) {
        showLoadingSpinner(); // Mostra lo spinner
    });
});


document.getElementById('logout').addEventListener('click', function() {
    fetch("/app_cucina/do_logout", {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,  // Use the token defined in the template
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // Check if the response contains a redirect URL
                if (data.redirect) {
                    window.location.href = data.redirect;  // Redirect to login page
                } else {
                    throw new Error(data.Error || 'Network response was not ok');
                }
            });
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // This will only execute if the logout is successful without errors
        window.location.href = "/app_cucina/login";  // Redirect to login page
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally redirect to login if there's a network error
        window.location.href = "/app_cucina/login";  // Redirect to login page
    });
});

