const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('alimentoForm');
    const submitButton = document.getElementById('submitButton');
    const alimentoIdField = document.getElementById('alimentoId');
    const addAlimentoModal = document.getElementById('addAlimentoModal');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddAlimentoForm = function() {
        form.reset(); // Resetta i campi del modulo
        alimentoIdField.value = ''; // Vuoto per indicare creazione
        submitButton.textContent = 'Aggiungi';
        document.getElementById('modalTitle').textContent = 'Aggiungi Allergene';
        addAlimentoModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaAlimentoForm = function(id) {
        fetch(`/app_cucina/allergeni/${id}`)
            .then(response => response.json())
            .then(data => {
                const alimento = data;
    
                // Popola i campi del modulo con i dati dell'alimento
                form.elements['nome'].value = alimento.nome;
    
                submitButton.textContent = 'Salva Modifiche';
                document.getElementById('modalTitle').textContent = 'Modifica Allergene';
                addAlimentoModal.style.display = 'block';
            })
            .catch(error => {
                console.error('Errore:', error);
                alert('Errore nel caricamento dei dati.');
            });
    };
    

    // Funzione per chiudere il modulo
    window.closeAddAlimentoForm = function() {
        addAlimentoModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce l'invio tradizionale del modulo
        const alimentoId = alimentoIdField.value;
        const url = alimentoId ? `/app_cucina/allergeni/${alimentoId}` : '/app_cucina/allergeni';
        const method = alimentoId ? 'PUT' : 'POST';
        const formData = new FormData(form);

        fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Operazione completata con successo!');
                closeAddAlimentoForm();
                location.reload(); // Ricarica la pagina per aggiornare la tabella
            } else {
                throw new Error('Errore durante la richiesta.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore durante l\'operazione.');
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const searchNameInput = document.getElementById('searchName');
   
   

    function filterTable() {
        const searchName = searchNameInput.value.toLowerCase();
       
        const rows = allergeniTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const nome = row.cells[1].textContent.toLowerCase(); // Nome nella prima colonna
           
            const matchesName = nome.includes(searchName);
            const matchesType = searchType === '' || tipo === searchTypeMap[searchType];

            if (matchesName && matchesType) {
                row.style.display = ''; // Mostra la riga
            } else {
                row.style.display = 'none'; // Nascondi la riga
            }
        }
    }

            /* eslint-disable */
// Funzione che costruisce la mappa `searchTypeMap` per le tipologie
function buildSearchTypeMap(tipologie) {
    const searchTypeMap = {};
    tipologie.forEach(function(tipologia) {
        searchTypeMap[tipologia.id] = tipologia.nome;
    });
    return searchTypeMap;
}

// Chiama la funzione passando i dati
const searchTypeMap = buildSearchTypeMap(tipologie);
console.log(searchTypeMap);  // Stampa la mappa per verificarne il contenuto


    // Event listener per i filtri
    searchNameInput.addEventListener('input', filterTable);
    searchTypeSelect.addEventListener('change', filterTable);
});


function eliminaAlimento(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        
        fetch(`/app_cucina/allergeni/${id}`, {  // Assicurati che l'URL sia corretto
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken // Includi solo il token CSRF
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
