document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('piattoForm');
    const submitButton = document.getElementById('submitButton');
    const piattoIdField = document.getElementById('piattoId');
    const addPiattoModal = document.getElementById('addModal');
    const searchNameInput = document.getElementById('searchName');
    const piattiTableBody = document.getElementById('piattiTableBody');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddForm = function() {
        form.reset();
        piattoIdField.value = '';
        submitButton.textContent = 'Aggiungi tipo Piatto';
        document.getElementById('modalTitle').textContent = 'Aggiungi tipo Piatto';
        addPiattoModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.showModificaForm = function(id) {
        fetch(`/app_cucina/tipologia_piatti/${id}`)
        .then(response => response.json())
        .then(data => {
            form.elements['color'].value = data.color;
            form.elements['backgroundColor'].value = data.backgroundColor;
            form.elements['descrizione'].value = data.descrizione;
            form.elements['descrizionePlurale'].value = data.descrizionePlurale;
            form.elements['inMenu'].checked = data.inMenu;
            form.elements['ordinatore'].value = data.ordinatore;
            piattoIdField.value = id;
            submitButton.textContent = 'Salva Modifiche';
            document.getElementById('modalTitle').textContent = 'Modifica tipo Piatto';
            addPiattoModal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching piatto data:', error);
        });
    };

    // Funzione per chiudere il modulo
    window.closeForm = function() {
        addPiattoModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const piattoId = piattoIdField.value;
        const url = piattoId ? `/app_cucina/tipologia_piatti/${piattoId}` : '/app_cucina/tipologia_piatti';
        const method = piattoId ? 'PUT' : 'POST';
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

    // Funzione per filtrare i piatti solo per nome
    function filterTable() {
        const searchName = searchNameInput.value.trim().toLowerCase();
        const rows = piattiTableBody.getElementsByTagName('tr');
        
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

    searchNameInput.addEventListener('input', filterTable);

});  

function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/tipologia_piatti/${id}`, {
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