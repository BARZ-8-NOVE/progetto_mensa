document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('serviziForm');
    const submitButton = document.getElementById('submitButton');
    const serviziIdField = document.getElementById('serviziId');
    const addModal = document.getElementById('addModal');
    const searchNameInput = document.getElementById('searchName');
    const serviziTableBody = document.getElementById('serviziTableBody');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddForm = function() {
        form.reset();
        serviziIdField.value = '';
        submitButton.textContent = 'Aggiungi Servizio';
        document.getElementById('modalTitle').textContent = 'Aggiungi Servizio';
        addModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaForm = function(id) {
        fetch(`/app_cucina/servizi/${id}`)
        .then(response => response.json())
        .then(data => {
            // Imposta i valori corretti nei campi del form
            form.elements['descrizione'].value = data.descrizione;
            form.elements['ordinatore'].value = data.ordinatore;   
            form.elements['inMenu'].checked = data.inMenu;

            serviziIdField.value = id;
            submitButton.textContent = 'Salva Modifiche';
            document.getElementById('modalTitle').textContent = 'Modifica Servizio';
            addModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Errore nel recupero dei dati del servizio:', error);
        });
    };

    // Funzione per chiudere il modulo
    window.closeForm = function() {
        addModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const serviziId = serviziIdField.value;
        const url = serviziId ? `/app_cucina/servizi/${serviziId}` : '/app_cucina/servizi';
        const method = serviziId ? 'PUT' : 'POST';
        const formData = new FormData(form);

        fetch(url, {
            method: method,
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Operazione completata con successo!');
                closeForm();
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

    // Funzione per filtrare i servizi per nome
    function filterTable() {
        const searchName = searchNameInput.value.trim().toLowerCase();
        const rows = serviziTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const servizioName = rows[i].getElementsByTagName('td')[1].textContent.toLowerCase();
            rows[i].style.display = servizioName.includes(searchName) ? '' : 'none';
        }
    }

    searchNameInput.addEventListener('input', filterTable);
});


function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/servizi/${id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken 
            }
        })
        .then(response => {
            if (response.ok) {
                alert('non puoi eliminare i servizi!');
                location.reload();
            } else {
                alert('Errore durante l\'eliminazione del record.');
            }
        })
        .catch(error => {
            console.error('Error during delete:', error);
        });
    }
}