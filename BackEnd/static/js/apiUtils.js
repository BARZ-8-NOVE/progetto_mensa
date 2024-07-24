// apiUtils.js

// Funzione per ottenere il token dalla variabile globale
function getToken() {
    return document.querySelector('script[data-token]').getAttribute('data-token');
}

// Funzione per eseguire chiamate API con il token
function fetchWithToken(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    return fetch(url, {
        ...options,
        headers
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;  // Redirect to login page
                } else {
                    throw new Error(data.Error || 'Network response was not ok');
                }
            });
        }
        return response.json();
    });
}

export { fetchWithToken };
