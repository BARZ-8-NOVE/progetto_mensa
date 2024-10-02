
function printProspetto(ordineId) {
    // Costruisci l'URL per la pagina di stampa
    var url = '/app_cucina/ordini/printProspetto/' + ordineId;

    // Apri una nuova finestra con la pagina di stampa
    var printWindow = window.open(url, '_blank', 'width=800,height=600');
    
    // Attendere che la finestra venga caricata
    printWindow.onload = function() {
        printWindow.print();
    };
}



function showForm(ordineId, servizioId, repartoId, schedaId) {
    const url = `ordini/schede_piatti/${ordineId}/${servizioId}/${repartoId}/${schedaId}`;
    console.log("Redirecting to URL: " + url);  // Aggiungi questo per vedere l'URL generato
    window.location.href = url;
}

function printPage(ordineId) {
    // Costruisci l'URL per la pagina di stampa
    var url = '/app_cucina/ordini/print/' + ordineId;

    // Apri una nuova finestra con la pagina di stampa
    var printWindow = window.open(url, '_blank', 'width=800,height=600');
    
    // Attendere che la finestra venga caricata
    printWindow.onload = function() {
        printWindow.print();
    };
}


function promptUpdateSchedaCount(ordineId, servizioId, repartoId, schedaId, currentValue) {
const newValue = prompt('Inserisci il nuovo valore:', currentValue);

if (newValue !== null && !isNaN(newValue)) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // Esegui una richiesta AJAX per inviare il nuovo valore al server
    fetch('/app_cucina/ordini/brodi', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken   // Aggiungi il token CSRF se necessario
        },
        body: JSON.stringify({
            ordineId: ordineId,
            servizioId: servizioId,
            reparto_id: repartoId,
            scheda_id: schedaId,

            new_count: newValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Ricarica la pagina per mostrare il nuovo valore
            location.reload();
        } else {
            console.error('Errore durante l\'aggiornamento del conteggio');
        }
    })
    .catch(error => console.error('Errore:', error));
}
}
