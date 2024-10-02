function updateTotalCaloriesDisplay() {
    // Aggiorna il contenuto del div con il totale delle calorie
    document.getElementById('calorieTotali').textContent = Math.round(totalCalories);
}

function toggleSelection(element, piattoId) {
    const calorie = parseInt(element.getAttribute('data-calorie')); // Ottieni le calorie dal data attribute

    // Rimuovi la selezione degli altri piatti dello stesso tipo
    const piattoType = element.getAttribute('data-type');
    const itemsToDeselect = Array.from(document.querySelectorAll(`.popup-item[data-type="${piattoType}"], .popup-custom-column-item[data-type="${piattoType}"]`));
    itemsToDeselect.forEach(item => {
        if (item.classList.contains('selezionato')) {
            item.classList.remove('selezionato');
            const index = selectedItems.findIndex(selectedItem => selectedItem.fkPiatto === parseInt(item.getAttribute('data-id')));
            if (index > -1) {
                totalCalories -= selectedItems[index].calorie; // Sottrai le calorie quando un piatto viene deselezionato
                selectedItems.splice(index, 1);
            }
        }
    });

    // Aggiungi o rimuovi la selezione per il piatto corrente
    element.classList.toggle('selezionato');
    const index = selectedItems.findIndex(item => item.fkPiatto === piattoId);
    
    if (index > -1) {
        // Se il piatto è già selezionato, rimuovilo e sottrai le calorie
        totalCalories -= selectedItems[index].calorie;
        selectedItems.splice(index, 1);
    } else {
        // Se il piatto non è selezionato, aggiungilo e somma le calorie
        totalCalories += calorie;
        selectedItems.push({ fkPiatto: piattoId, quantita: 1, note: "", calorie: calorie }); // Aggiungi calorie all'oggetto
    }
    
    console.log(selectedItems);
    console.log(`Calorie totali: ${totalCalories}`); // Stampa il totale calorico
    updateHiddenField();
    toggleSubmitButton();
    updateTotalCaloriesDisplay(); // Aggiorna il totale delle calorie nel DOM
}

// Funzione per aggiornare il campo nascosto
function updateHiddenField() {
    document.getElementById('piattiList').value = JSON.stringify(selectedItems);
}

// Funzione per attivare/disattivare il bottone di invio
function toggleSubmitButton() {
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = selectedItems.length === 0; // Disattiva il pulsante se non ci sono piatti selezionati
}

// Inizializza la selezione all'apertura del popup
document.querySelectorAll('.popup-item, .popup-custom-column-item').forEach(item => {
    const piattoId = parseInt(item.getAttribute('data-id'));
    if (selectedItems.find(item => item.fkPiatto === piattoId)) {
        item.classList.add('selezionato');
    }
});

// Inizializza il display delle calorie totali
updateTotalCaloriesDisplay();


function elimina(ordine_id) {
    if (confirm('Sei sicuro di voler eliminare questo record?')) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        fetch(`/app_cucina/ordini/delete/${ordine_id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken 
            }
        })
        .then(response => {
            if (response.ok) {
                // Notifica di successo
                alert('Record eliminato con successo.');
                // Ricarica la pagina per aggiornare i dati
                location.reload();
            } else {
                // Notifica di errore
                alert('Errore durante l\'eliminazione del record.');
            }
        })
        .catch(error => {
            console.error('Error during delete:', error);
            alert('Errore durante l\'eliminazione del record.');
        });
    }
}