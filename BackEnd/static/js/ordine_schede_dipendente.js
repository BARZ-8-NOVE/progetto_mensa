
function toggleSelection(element, piattoId) {
    const piattoType = element.getAttribute('data-type'); // Assicurati che il tuo elemento abbia questo attributo
    
    // Rimuovi la selezione degli altri piatti dello stesso tipo
    const itemsToDeselect = Array.from(document.querySelectorAll(`.popup-item[data-type="${piattoType}"], .popup-custom-column-item[data-type="${piattoType}"]`));
    itemsToDeselect.forEach(item => {
        if (item.classList.contains('selezionato')) {
            item.classList.remove('selezionato');
            const index = selectedItems.findIndex(selectedItem => selectedItem.fkPiatto === parseInt(item.getAttribute('data-id')));
            if (index > -1) {
                selectedItems.splice(index, 1);
            }
        }
    });
    
    // Aggiungi o rimuovi la selezione per il piatto corrente
    element.classList.toggle('selezionato');
    const index = selectedItems.findIndex(item => item.fkPiatto === piattoId);
    
    if (index > -1) {
        selectedItems.splice(index, 1);
    } else {
        selectedItems.push({ fkPiatto: piattoId, quantita: 1, note: "" });
    }
    
    updateHiddenField();
    toggleSubmitButton();
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