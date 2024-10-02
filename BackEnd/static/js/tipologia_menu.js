document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('menuForm');
    const submitButton = document.getElementById('submitButton');
    const tipoMuneIdField = document.getElementById('menuId');
    const addmenuModal = document.getElementById('addModal');
    const searchNameInput = document.getElementById('searchName');
    const menuTableBody = document.getElementById('menuTableBody');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddForm = function() {
        form.reset();
        tipoMuneIdField.value = '';
        submitButton.textContent = 'Aggiungi tipo Menu';
        document.getElementById('modalTitle').textContent = 'Aggiungi tipo Menu';
        addmenuModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaForm = function(id) {
        fetch(`/app_cucina/tipologia_menu/${id}`)
        .then(response => response.json())
        .then(data => {
            // Imposta i valori corretti nei campi del form
            form.elements['backgroundColor'].value = data.backgroundColor;  // Assicurati che il campo nel JSON sia 'backgroundColor'
            form.elements['descrizione'].value = data.descrizione;
            form.elements['ordinatore'].value = data.ordinatore;
            tipoMuneIdField.value = id;
            submitButton.textContent = 'Salva Modifiche';
            document.getElementById('modalTitle').textContent = 'Modifica tipo Menu';
            addmenuModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching Menu data:', error);
        });
    };

    // Funzione per chiudere il modulo
    window.closeForm = function() {
        addmenuModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const menuId = tipoMuneIdField.value;
        const url = menuId ? `/app_cucina/tipologia_menu/${menuId}` : '/app_cucina/tipologia_menu';
        const method = menuId ? 'PUT' : 'POST';
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

    // Funzione per filtrare i menu solo per nome
    function filterTable() {
        const searchName = searchNameInput.value.trim().toLowerCase();
        const rows = menuTableBody.getElementsByTagName('tr');
        
        for (let i = 0; i < rows.length; i++) {
            const nameCell = rows[i].getElementsByTagName('td')[2]; // Colonna 'Descrizione'
            const nameMatches = nameCell && nameCell.textContent.trim().toLowerCase().includes(searchName);
            
            if (nameMatches) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }

    searchNameInput.addEventListener('input', filterTable);

});  

function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/tipologia_menu/${id}`, {
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