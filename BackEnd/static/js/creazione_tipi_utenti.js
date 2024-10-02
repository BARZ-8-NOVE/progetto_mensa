document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('userTypeForm');
    const submitButton = document.getElementById('submitButton');
    const tipoUtenteIdField = document.getElementById('tipoUtenteId');
    const addUtenteModal = document.getElementById('addUtenteModal');
    const permissionItems = document.getElementById('permissionItems');

    // Funzione per mostrare il modulo di aggiunta
    window.showAddUtenteForm = function() {
        form.reset(); // Resetta i campi del modulo
        tipoUtenteIdField.value = ''; // Vuoto per indicare creazione
        submitButton.textContent = 'Aggiungi';
        document.getElementById('modalTitle').textContent = 'Aggiungi Tipo Utente';
        permissionItems.querySelectorAll('input[type="checkbox"]').forEach(checkbox => checkbox.checked = false);
        addUtenteModal.style.display = 'block';
    };

    // Funzione per aprire il modulo di modifica
    window.openEditUtenteForm = function(id) {
        fetch(`/app_cucina/creazione_tipologia_utenti/${id}`)
            .then(response => response.json())
            .then(data => {
                const tipoUtente = data.tipo_utente;
                const funzionalitaMap = data.funzionalita;
                const funzionalitaAssociate = data.funzionalita_associate;

                // Popola il campo del nome del tipo utente
                document.querySelector('[name="fkTipoUtente"]').value = tipoUtente.nomeTipoUtente;
                tipoUtenteIdField.value = tipoUtente.id;

                // Popola le funzionalità e i permessi
                permissionItems.innerHTML = '';
                Object.keys(funzionalitaMap).forEach(funz_id => {
                    const funz_titolo = funzionalitaMap[funz_id];
                    const funzionalitaChecked = funzionalitaAssociate.some(f => f.fkFunzionalita == funz_id);
                    const permessiChecked = funzionalitaAssociate.some(f => f.fkFunzionalita == funz_id && f.permessi);

                    const permissionOption = document.createElement('div');
                    permissionOption.classList.add('permission-option');
                    permissionOption.innerHTML = `
                        <label>
                            <input type="checkbox" name="funzionalita" value="${funz_id}" ${funzionalitaChecked ? 'checked' : ''}>
                            ${funz_titolo}
                            <input type="checkbox" name="permesso_${funz_id}" value="true" ${permessiChecked ? 'checked' : ''}> Abilitato
                        </label>
                    `;
                    permissionItems.appendChild(permissionOption);
                });

                submitButton.textContent = 'Salva Modifiche';
                document.getElementById('modalTitle').textContent = 'Modifica Tipo Utente';
                addUtenteModal.style.display = 'block';
            });
    };

    // Funzione per chiudere il modulo
    window.closeAddUtenteForm = function() {
        addUtenteModal.style.display = 'none';
    };

    // Gestione dell'invio del modulo
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce l'invio del modulo tradizionale
        const tipoUtenteId = tipoUtenteIdField.value;
        const url = tipoUtenteId ? `/app_cucina/creazione_tipologia_utenti/${tipoUtenteId}` : '/app_cucina/creazione_tipologia_utenti';
        const method = tipoUtenteId ? 'PUT' : 'POST';
        const formData = new FormData(form);

        fetch(url, {
            method: method,
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Operazione completata con successo!');
                closeAddUtenteForm();

                // Ricarica la pagina per aggiornare la tabella
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

    

    // Funzione per filtrare la tabella
    function filterTable() {
        const searchName = document.getElementById('searchName').value.toLowerCase();
        const rows = document.getElementById('utentiTableBody').getElementsByTagName('tr');
        Array.from(rows).forEach(row => {
            const username = row.cells[1].textContent.toLowerCase();
            row.style.display = username.includes(searchName) ? '' : 'none';
        });
    }

    // Aggiungi eventi ai campi di ricerca
    document.getElementById('searchName').addEventListener('keyup', filterTable);
});


function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`/app_cucina/creazione_tipologia_utenti/${id}`, {
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