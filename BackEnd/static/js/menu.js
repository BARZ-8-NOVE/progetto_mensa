function showMenuForm(id_menu) {
    if (id_menu !== 'null') {
        window.location.href = '/app_cucina/menu/dettagli/' + id_menu;
    } else {
        alert('Nessun menu disponibile.');
    }
}

function prepareClone(menuId) {
    // Ottieni i parametri della query string dalla URL corrente
    const urlParams = new URLSearchParams(window.location.search);
    const nextUrl = `/app_cucina/menu?${urlParams.toString()}`;

    // Imposta il valore del campo nascosto per l'ID del menu da clonare
    document.getElementById('menu_id_to_clone').value = menuId;

    // Imposta il valore del campo nascosto per l'URL di ritorno
    document.getElementById('next_url').value = nextUrl;

    // Mostra il modulo di clonazione
    document.getElementById('clonaModal').style.display = 'block';
}

function closeClonaForm() {
    console.log('Chiusura del popup.');
    document.getElementById('clonaModal').style.display = 'none';
}

function deleteMenu(menuId) {
    if (confirm('Sei sicuro di voler eliminare questo Menu?')) {
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/menu/${menuId}`, {  // Aggiungi il prefisso /app_cucina/
            method: 'DELETE',
            headers: {
                
                'X-CSRFToken': csrfToken // Includi il token CSRF negli headers
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Menu eliminato con successo.');
                location.reload();
            } else {
                alert('Errore durante l\'eliminazione del Menu.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore di rete durante l\'eliminazione del Menu.');
        });
    }
}



function showClonaMeseForm() {
    const urlParams = new URLSearchParams(window.location.search);
    const nextUrl = `/app_cucina/menu?${urlParams.toString()}`;
    
    document.getElementById('clona_mese_next_url').value = nextUrl;
    document.getElementById('clonaMeseModal').style.display = 'block';
}

function closeClonaMeseModal() {
    document.getElementById('clonaMeseModal').style.display = 'none';
}