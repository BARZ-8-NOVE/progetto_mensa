function showAddSchedaForm() {
    const form = document.getElementById('schedaForm');
    form.action = 'schede';
    document.getElementById('modalTitle').textContent = 'Aggiungi Scheda';
    document.getElementById('submitButton').textContent = 'Aggiungi';
    resetForm(form);
    document.getElementById('SchedaModal').style.display = 'block';
}


function elimina(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch(`schede/${id}`, {
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


function showModificaSchedaForm(id) {
    fetch(`schede/${id}`)
        .then(response => response.json())
        .then(data => {
            const form = document.getElementById('schedaForm');
            form.action = `schede/${id}`;
            document.getElementById('modalTitle').textContent = 'Modifica Scheda';
            document.getElementById('submitButton').textContent = 'Salva Modifiche';

            form.elements['backgroundColor'].value = data.backgroundColor;
            form.elements['fkTipoAlimentazione'].value = data.fkTipoAlimentazione;
            form.elements['fkTipoMenu'].value = data.fkTipoMenu;
            form.elements['nome'].value = data.nome;
            form.elements['titolo'].value = data.titolo;
            form.elements['sottotitolo'].value = data.sottotitolo;
            form.elements['descrizione'].value = data.descrizione;
            form.elements['dipendente'].checked = data.dipendente;
            form.elements['nominativa'].checked = data.nominativa;
            form.elements['inizio'].value = data.inizio;
            form.elements['fine'].value = data.fine;
            form.elements['note'].value = data.note;

            document.getElementById('SchedaModal').style.display = 'block';
        });
}

function closeModal() {
    document.getElementById('SchedaModal').style.display = 'none';
}

function resetForm(form) {
    form.reset();
    Array.from(form.elements).forEach(element => {
        if (element.type === 'checkbox') {
            element.checked = false;
        }
    });
}

window.onclick = function(event) {
    const modal = document.getElementById("SchedaModal");
    if (event.target === modal) {
        closeModal();
    }
}

window.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeModal();
    }
});

function showAddSchedaPiattiForm(schedaId) {
    window.location.href = `schede/piatti/${schedaId}`;
}

function showAddSchedapreconfezionataForm(schedaId) {
    window.location.href = `schede/schedepreconfezionate/${schedaId}`;
}