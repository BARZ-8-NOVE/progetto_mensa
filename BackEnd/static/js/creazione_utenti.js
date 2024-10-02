const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// Funzione per aprire il modulo di aggiunta utente
function showAddUtenteForm() {
    document.getElementById('addUtenteModal').style.display = 'block';
}

function closeAddUtenteForm() {
    document.getElementById('addUtenteModal').style.display = 'none';
}

// Funzione per aprire il modulo di modifica
function showModificaForm(public_id) {
console.log(`Fetching data for user with public_id: ${public_id}`);

fetch(`/app_cucina/creazione_utenti/${public_id}`)
.then(response => {
    console.log('Response status:', response.status);
    if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.statusText);
    }
    return response.json();
})
.then(data => {
    console.log('Received user data:', data);

    // Popola i campi del form con i dati ricevuti
    document.getElementById('editUsername').value = data.username;
    document.getElementById('editNome').value = data.nome;
    document.getElementById('editCognome').value = data.cognome;
    document.getElementById('editEmail').value = data.email;
    document.getElementById('editUtenteId').value = public_id;

    // Aggiorna il valore dei campi del form
    const form = document.querySelector('#editUtenteForm');
    form.elements['fkTipoUtente'].value = data.fkTipoUtente;
    form.elements['inizio'].value = data.inizio;
    form.elements['fine'].value = data.fine;

    // Popola le checkbox dei reparti
    const repartiCheckboxes = document.querySelectorAll('input[name="reparti"]');
    const repartiSelected = data.reparti; // Assicurati che 'reparti' sia un array
    console.log('Selected departments:', repartiSelected);

    repartiCheckboxes.forEach(checkbox => {
        console.log(`Checkbox for department ${checkbox.value} is being checked/unchecked`);
        if (repartiSelected.includes(checkbox.value)) {
            checkbox.checked = true;  // Se il reparto è presente, seleziona la checkbox
            console.log(`Checked: ${checkbox.value}`);
        } else {
            checkbox.checked = false; // Altrimenti, deseleziona
            console.log(`Unchecked: ${checkbox.value}`);
        }
    });

    // Mostra il modal
    document.getElementById('editUtenteModal').style.display = 'block';
    console.log('Edit user modal is now displayed.');
})
.catch(error => {
    console.error('Error fetching Utente data:', error);
});
}


// Memorizza i valori iniziali dei checkbox al caricamento della pagina o all'apertura del modal
let initialCheckboxValues = new Set();

document.addEventListener('DOMContentLoaded', () => {
 // Popola i valori iniziali
 document.querySelectorAll('input[name="reparti"]:checked').forEach(checkbox => {
     initialCheckboxValues.add(checkbox.value);
 });
});

// Funzione per gestire l'aggiornamento dell'utente
document.querySelector('#editUtenteForm').addEventListener('submit', function(event) {
event.preventDefault(); // Previeni l'invio del form di default

// Ottieni l'ID dell'utente
const public_id = document.getElementById('editUtenteId').value;
const formData = new FormData(this);

const repartiValues = [];

// Cicla su tutte le voci di FormData
for (let [key, value] of formData.entries()) {
    // Filtra solo le voci che corrispondono a 'reparti'
    if (key.startsWith('reparti')) {
        repartiValues.push(value);
        console.log(`Reparti: ${value}`);
    }
}

// Se hai più checkbox per 'reparti', potresti trovare più voci
console.log('Tutti i valori di reparti:', repartiValues);


const payload = {
    public_id: public_id,
    fkTipoUtente: formData.get('fkTipoUtente'),
    reparti: repartiValues,  // Usa l'array di nuovi reparti
    inizio: formData.get('inizio'),
    fine: formData.get('fine')
};

// Aggiungi il token CSRF all'intestazione della richiesta


// Invia la richiesta di aggiornamento
fetch(`/app_cucina/creazione_utenti/${public_id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    }
})
.then(response => response.text()) // Recupera la risposta come testo
.then(text => {
    console.log('Server Response:', text);
    
    // Prova a fare il parsing della risposta in JSON
    let data;
    try {
        data = JSON.parse(text); 
    } catch (e) {
        console.error('Errore nel parsing della risposta:', e);
        alert('Errore nella risposta del server');
        return;
    }

    // Controlla se esiste un messaggio di successo
    if (data.message && data.message.includes('aggiornato con successo')) {
        alert('Utente aggiornato con successo');
        closeEditUtenteForm(); // Chiudi il modal
        
        // Ricarica la pagina per aggiornare i dati
        location.reload(); 
    } else {
        alert('Errore nell\'aggiornamento dell\'utente');
    }
})
.catch(error => {
    console.error('Errore durante l\'aggiornamento dell\'utente:', error);
    alert('Errore di rete o server');
});



});

function closeEditUtenteForm() {
    document.getElementById('editUtenteModal').style.display = 'none';
}

// Funzione per filtrare la tabella
document.addEventListener('DOMContentLoaded', function() {
    const searchNameInput = document.getElementById('searchName');
    const searchTypeSelect = document.getElementById('searchType');
    const utentiTableBody = document.getElementById('utentiTableBody');

    function filterTable() {
        const searchName = searchNameInput.value.toLowerCase();
        const searchType = searchTypeSelect.value;

        const rows = utentiTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const username = row.cells[1].textContent.toLowerCase(); // Nome nella seconda colonna
            const fkTipoUtente = row.cells[4].textContent; // Ruolo nella quinta colonna

            const matchesName = username.includes(searchName);
            const matchesType = searchType === '' || fkTipoUtente === searchTypeSelect.options[searchTypeSelect.selectedIndex].text;

            if (matchesName && matchesType) {
                row.style.display = ''; // Mostra la riga
            } else {
                row.style.display = 'none'; // Nascondi la riga
            }
        }
    }

    // Aggiungi eventi ai campi di ricerca
    searchNameInput.addEventListener('keyup', filterTable);
    searchTypeSelect.addEventListener('change', filterTable);
});



function impersonifica(public_id) {
    console.log("Impersonificazione utente con public_id:", public_id);

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    if (confirm("Vuoi impersonare questo utente?")) {
        fetch(`/app_cucina/creazione_utenti/impersonate/${public_id}`, {
            method: 'POST',
            headers: {

                'X-CSRFToken': csrfToken  
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {

                window.location.href = '/app_cucina/home';

            } else {
                alert('Errore durante l\'impersonificazione.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore durante la richiesta.');
        });
    }
}


