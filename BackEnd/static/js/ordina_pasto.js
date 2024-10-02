function showForm2(schedaId, id, repartoId, servizioId) {
 

    // Costruisci l'URL con i parametri nell'ordine corretto
    let url = `/app_cucina/ordina_pasto/schede_dipendente/${id}/${servizioId}/${repartoId}/${schedaId}`;
    window.location.href = url;
}


function modifica(id, servizio, reparto, scheda, ordine_id) {
    const url = `/app_cucina/ordina_pasto/schede_dipendente/${id}/${servizio}/${reparto}/${scheda}/${ordine_id}`;
    console.log("Redirecting to URL: " + url);  // Aggiungi questo per vedere l'URL generato
    window.location.href = url;
}


function elimina(ordine_id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/ordini/delete/${ordine_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken 
            }
        })
        .then(response => {
            if (response.ok) {
                // Notifica di successo
                alert('Record eliminato con successo.');
                // Ricarica la pagina per aggiornare i dati
                location.reload();
            } else {
                // Notifica di errore
                alert('Errore durante l\'eliminazione del record.');
            }
        })
        .catch(error => {
            console.error('Error during delete:', error);
            alert('Errore durante l\'eliminazione del record.');
        });
    }
}
