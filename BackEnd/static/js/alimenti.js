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
        document.getElementById('modalTitle').textContent = 'Aggiungi Alimento';
        addAlimentoModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaAlimentoForm = function(id) {
        fetch(`/app_cucina/alimenti/${id}`)
            .then(response => response.json())
            .then(data => {
                const alimento = data;
    
                // Popola i campi del modulo con i dati dell'alimento
                form.elements['alimento'].value = alimento.alimento;
                form.elements['energia_Kcal'].value = alimento.energia_Kcal;
                form.elements['energia_KJ'].value = alimento.energia_KJ;
                form.elements['prot_tot_gr'].value = alimento.prot_tot_gr;
                form.elements['glucidi_tot'].value = alimento.glucidi_tot;
                form.elements['lipidi_tot'].value = alimento.lipidi_tot;
                form.elements['saturi_tot'].value = alimento.saturi_tot;
                form.elements['fkTipologiaAlimento'].value = alimento.fkTipologiaAlimento;
    
                // Gestione dei checkbox per gli allergeni
                const allergeniSelezionati = alimento.fkAllergene.split(',');  // Es. "1,4,7"
                const fkAllergeneCheckboxes = form.elements['fkAllergene'];  // Checkbox multipli
    
                for (let i = 0; i < fkAllergeneCheckboxes.length; i++) {
                    if (allergeniSelezionati.includes(fkAllergeneCheckboxes[i].value)) {
                        fkAllergeneCheckboxes[i].checked = true;
                    } else {
                        fkAllergeneCheckboxes[i].checked = false;
                    }
                }
    
                alimentoIdField.value = id; // Imposta l'ID dell'alimento per la modifica
    
                submitButton.textContent = 'Salva Modifiche';
                document.getElementById('modalTitle').textContent = 'Modifica Alimento';
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
        const url = alimentoId ? `/app_cucina/alimenti/${alimentoId}` : '/app_cucina/alimenti';
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
    const searchTypeSelect = document.getElementById('searchType');
    const alimentiTableBody = document.getElementById('alimentiTableBody');

    function filterTable() {
        const searchName = searchNameInput.value.toLowerCase();
        const searchType = searchTypeSelect.value;

        const rows = alimentiTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const nome = row.cells[1].textContent.toLowerCase(); // Nome nella prima colonna
            const tipo = row.cells[9].textContent; // Tipologia nella nona colonna

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



document.getElementById('allergeni').addEventListener('change', function () {
    const selectedAllergens = Array.from(this.selectedOptions).map(option => option.text);
    const selectedAllergensList = document.getElementById('selectedAllergensList');
    selectedAllergensList.innerHTML = '';
    selectedAllergens.forEach(allergene => {
        const li = document.createElement('li');
        li.textContent = allergene;
        selectedAllergensList.appendChild(li);
    });
});


function eliminaAlimento(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        
        fetch(`/app_cucina/alimenti/${id}`, {  // Assicurati che l'URL sia corretto
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
