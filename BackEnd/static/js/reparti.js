document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('repartiForm');
    const submitButton = document.getElementById('submitButton');
    const tipoIdField = document.getElementById('repartiId');
    const addRepartiModal = document.getElementById('addModal');
    const searchNameInput = document.getElementById('searchName');
    const repartiTableBody = document.getElementById('repartiTableBody');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddForm = function() {
        form.reset();
        tipoIdField.value = '';
        submitButton.textContent = 'Aggiungi Reparto';
        document.getElementById('modalTitle').textContent = 'Aggiungi Reparto';
        addRepartiModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaForm = function(id) {
        fetch(`/app_cucina/reparti/${id}`)
        .then(response => response.json())
        .then(data => {
            // Imposta i valori corretti nei campi del form
            form.elements['codiceAreas'].value = data.codiceAreas;
            form.elements['descrizione'].value = data.descrizione;
            form.elements['sezione'].value = data.sezione;
            form.elements['ordinatore'].value = data.ordinatore;
            form.elements['padiglione'].value = data.padiglione;
            form.elements['piano'].value = data.piano;
            form.elements['lato'].value = data.lato;
            form.elements['inizio'].value = data.inizio;
            form.elements['fine'].value = data.fine;

            tipoIdField.value = id;
            submitButton.textContent = 'Salva Modifiche';
            document.getElementById('modalTitle').textContent = 'Modifica Reparto';
            addRepartiModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching reparto data:', error);
        });
    };

    // Funzione per chiudere il modulo
    window.closeForm = function() {
        addRepartiModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const repartoId = tipoIdField.value;
        const url = repartoId ? `/app_cucina/reparti/${repartoId}` : '/app_cucina/reparti';
        const method = repartoId ? 'PUT' : 'POST';
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

    // Funzione per filtrare i reparti solo per nome
    function filterTable() {
        const searchName = searchNameInput.value.trim().toLowerCase();
        const rows = repartiTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const repartoName = rows[i].getElementsByTagName('td')[1].textContent.toLowerCase();
            rows[i].style.display = repartoName.includes(searchName) ? '' : 'none';
        }
    }

    searchNameInput.addEventListener('input', filterTable);
});
   

function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/reparti/${id}`, {
            method: 'DELETE',
            headers: {

                'X-CSRFToken': csrfToken 
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Record eliminato con successo.');
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