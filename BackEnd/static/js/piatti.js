document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('piattoForm');
    const submitButton = document.getElementById('submitButton');
    const piattoIdField = document.getElementById('piattoId');
    const addPiattoModal = document.getElementById('addPiattoModal');
    const searchNameInput = document.getElementById('searchName');  // Aggiunto correttamente
    const searchTypeSelect = document.getElementById('searchType'); // Aggiunto correttamente
    const piattiTableBody = document.getElementById('piattiTableBody'); // Tabella piatti

    // Funzione per mostrare il modulo di aggiunta
    window.showAddForm = function() {
        form.reset(); // Resetta i campi del modulo
        piattoIdField.value = ''; // Vuoto per indicare creazione
        submitButton.textContent = 'Aggiungi Piatto';
        document.getElementById('modalTitle').textContent = 'Aggiungi Piatto';
        addPiattoModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaForm = function(id) {
        fetch(`/app_cucina/piatti/${id}`)
        .then(response => response.json())
        .then(data => {
            form.elements['fkTipoPiattoSelect'].value = data.fkTipoPiatto;
            form.elements['codice'].value = data.codice;
            form.elements['titolo'].value = data.titolo;
            form.elements['descrizione'].value = data.descrizione;
            form.elements['inMenu'].checked = data.inMenu;
            form.elements['ordinatore'].value = data.ordinatore;
            piattoIdField.value = id;
            submitButton.textContent = 'Salva Modifiche';
            document.getElementById('modalTitle').textContent = 'Modifica Piatto';
            addPiattoModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching piatto data:', error);
        });
    };

    // Funzione per chiudere il modulo
    window.closeAddPiattoForm = function() {
        addPiattoModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const piattoId = piattoIdField.value;
        const url = piattoId ? `/app_cucina/piatti/${piattoId}` : '/app_cucina/piatti';
        const method = piattoId ? 'PUT' : 'POST';
        const formData = new FormData(form);

        fetch(url, {
            method: method,
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Operazione completata con successo!');
                closeAddPiattoForm();
                location.reload();
            } else {
                throw new Error('Errore durante la richiesta.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore durante l\'operazione.');
        });
    });

    // Funzione per filtrare i piatti
    function filterTable() {
        const searchName = searchNameInput.value.trim().toLowerCase();
        const searchType = searchTypeSelect.value;

        const rows = piattiTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const nome = row.cells[3].textContent.trim().toLowerCase(); // Nome del piatto nella quarta colonna
            const tipo = row.cells[1].textContent.trim(); // Tipo del piatto nella seconda colonna

            const matchesName = nome.includes(searchName);
            const matchesType = searchType === '' || tipo === searchTypeMap[searchType];

            if (matchesName && matchesType) {
                row.style.display = ''; // Mostra la riga
            } else {
                row.style.display = 'none'; // Nascondi la riga
            }
        }
    }

    // Mappa per i tipi di piatto


    // Event listener per i filtri
    searchNameInput.addEventListener('input', filterTable);
    searchTypeSelect.addEventListener('change', filterTable);
});

function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`piatti/${id}`, {
            method: 'DELETE',
            headers: {

                'X-CSRFToken': csrfToken // Includi il token CSRF negli headers
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Record eliminato con successo.');
                // Ricarica o aggiorna la pagina dopo l'eliminazione
                location.reload(); // O usa `window.location.href` se non vuoi ricaricare l'intera pagina
            } else {
                alert('Errore durante l\'eliminazione del record.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore di rete durante l\'eliminazione del record.');
        });
    }
}