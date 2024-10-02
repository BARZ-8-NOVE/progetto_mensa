
function eliminaAlimento(id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
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
            const nome = row.cells[0].textContent.toLowerCase(); // Nome nella prima colonna
            const tipo = row.cells[8].textContent; // Tipologia nella nona colonna

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


    // Event listener per i filtri
    searchNameInput.addEventListener('input', filterTable);
    searchTypeSelect.addEventListener('change', filterTable);
});

function showAddAlimentoForm() {
    document.getElementById('addAlimentoModal').style.display = 'block';
}

function closeAddAlimentoForm() {
    document.getElementById('addAlimentoModal').style.display = 'none';
}

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