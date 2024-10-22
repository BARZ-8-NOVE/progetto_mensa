const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

document.addEventListener('DOMContentLoaded', function() {
    // Elements for Metodo di Conservazione modal
    const conservazioneForm = document.getElementById('conservazioneForm');
    const conservazioneIdField = document.getElementById('conservazioneId');
    const conservazioneModal = document.getElementById('addConservazioneModal');
    const conservazioneSubmitButton = document.getElementById('submitButton');
    
    const searchtipologiaInput = document.getElementById('searchTipologia');
    const searchmetodoInput = document.getElementById('searchMetodo');
    // Elements for Tipologia Alimento modal
    const tipologiaAlimentoForm = document.getElementById('tipologiaAlimentoForm');
    const tipologiaAlimentoIdField = document.getElementById('tipologiaAlimentoId');
    const tipologiaAlimentoModal = document.getElementById('addTipologiaAlimentoModal');
    const tipologiaAlimentoSubmitButton = document.getElementById('submitButton');

    // 1. Functions for Metodo di Conservazione Modal

    // Show the modal for adding a new Metodo di Conservazione
    window.showAddConservazioneForm = function() {
        conservazioneForm.reset(); // Reset form fields
        conservazioneIdField.value = ''; // Empty the ID field for creation
        conservazioneSubmitButton.textContent = 'Aggiungi Metodo di Conservazione';
        document.getElementById('modalTitle').textContent = 'Aggiungi Metodo di Conservazione';
        conservazioneModal.style.display = 'block'; // Show the modal
    };

    // Show the modal for editing an existing Metodo di Conservazione
    window.showModificaConservazioneForm = function(id) {
        fetch(`/app_cucina/tipologia_alimenti/metodo_conservazione/${id}`)
            .then(response => response.json())
            .then(data => {
                // Populate the form with the fetched data
                conservazioneForm.elements['nome'].value = data.nome;
                conservazioneIdField.value = id;
                conservazioneSubmitButton.textContent = 'Salva Modifiche';
                document.getElementById('modalTitle').textContent = 'Modifica Metodo di Conservazione';
                conservazioneModal.style.display = 'block'; // Show the modal
            })
            .catch(error => {
                console.error('Errore:', error);
                alert('Errore nel caricamento dei dati.');
            });
    };

    // Close the Metodo di Conservazione modal
    window.closeAddConservazioneForm = function() {
        conservazioneModal.style.display = 'none';
    };

    // Form submission for Metodo di Conservazione
    conservazioneForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const conservazioneId = conservazioneIdField.value;
        const url = conservazioneId ? `/app_cucina/tipologia_alimenti/metodo_conservazione/${conservazioneId}` : '/app_cucina/tipologia_alimenti';
        const method = conservazioneId ? 'PUT' : 'POST';
        const formData = new FormData(conservazioneForm);

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
                closeAddConservazioneForm();
                location.reload(); // Reload the page to update the table
            } else {
                throw new Error('Errore durante la richiesta.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore durante l\'operazione.');
        });
    });

    // 2. Functions for Tipologia Alimento Modal

    // Show the modal for adding a new Tipologia Alimento
    window.showAddTipologiaAlimentoForm = function() {
        tipologiaAlimentoForm.reset(); // Reset form fields
        tipologiaAlimentoIdField.value = ''; // Empty the ID field for creation
        tipologiaAlimentoSubmitButton.textContent = 'Aggiungi Tipologia Alimento';
        document.getElementById('modalTipoTitle').textContent = 'Aggiungi Tipologia Alimento';
        tipologiaAlimentoModal.style.display = 'block'; // Show the modal
    };

    // Show the modal for editing an existing Tipologia Alimento
    window.showModificaTipologiaAlimentoForm = function(id) {
        fetch(`/app_cucina/tipologia_alimenti/${id}`)
            .then(response => response.json())
            .then(data => {
                // Populate the form with the fetched data
                tipologiaAlimentoForm.elements['nome'].value = data.nome;
                tipologiaAlimentoForm.elements['fktipologiaConservazione'].value = data.fktipologiaConservazione;
                tipologiaAlimentoIdField.value = id;
                tipologiaAlimentoSubmitButton.textContent = 'Salva Modifiche';
                document.getElementById('modalTipoTitle').textContent = 'Modifica Tipologia Alimento';
                tipologiaAlimentoModal.style.display = 'block'; // Show the modal
            })
            .catch(error => {
                console.error('Errore:', error);
                alert('Errore nel caricamento dei dati.');
            });
    };

    // Close the Tipologia Alimento modal
    window.closeAddTipologiaAlimentoForm = function() {
        tipologiaAlimentoModal.style.display = 'none';
    };

    // Form submission for Tipologia Alimento
    tipologiaAlimentoForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const tipologiaAlimentoId = tipologiaAlimentoIdField.value;
        const url = tipologiaAlimentoId ? `/app_cucina/tipologia_alimenti/${tipologiaAlimentoId}` : '/app_cucina/tipologia_alimenti';
        const method = tipologiaAlimentoId ? 'PUT' : 'POST';
        const formData = new FormData(tipologiaAlimentoForm);

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
                closeAddTipologiaAlimentoForm();
                location.reload(); // Reload the page to update the table
            } else {
                throw new Error('Errore durante la richiesta.');
            }
        })
        .catch(error => {
            console.error('Errore:', error);
            alert('Errore durante l\'operazione.');
        });

    });
    


    // Funzione per filtrare i piatti solo per nome
    function filterTable() {
        const searchName = searchtipologiaInput.value.trim().toLowerCase();
        const rows = metodoTableBody.getElementsByTagName('tr');
        
        for (let i = 0; i < rows.length; i++) {
            const nameCell = rows[i].getElementsByTagName('td')[1]; // Colonna 'Descrizione'
            const nameMatches = nameCell && nameCell.textContent.trim().toLowerCase().includes(searchName);
            
            if (nameMatches) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }

    searchtipologiaInput.addEventListener('input', filterTable);

    // Funzione per filtrare i piatti solo per nome
    function filterTable() {
        const searchName = searchmetodoInput.value.trim().toLowerCase();
        const rows = tipologiaTableBody.getElementsByTagName('tr');
        
        for (let i = 0; i < rows.length; i++) {
            const nameCell = rows[i].getElementsByTagName('td')[1]; // Colonna 'Descrizione'
            const nameMatches = nameCell && nameCell.textContent.trim().toLowerCase().includes(searchName);
            
            if (nameMatches) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }

    searchmetodoInput.addEventListener('input', filterTable);

});  

