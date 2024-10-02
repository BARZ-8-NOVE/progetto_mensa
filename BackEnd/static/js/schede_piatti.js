let currentPiattoId = null;
const schedaId = document.body.getAttribute('data-scheda-id');

function showPiattoModal(piattoId = null) {
    const modal = document.getElementById('piattoModal');
    const form = document.getElementById('piattoForm');
    const modalTitle = document.getElementById('piattoModalTitle');
    const piattoIdInput = document.getElementById('piattoId');
    const submitButton = form.querySelector('input[type="submit"]');
    const servizioId = document.querySelector('select[name="servizio"]').value;

    if (piattoId) {
        // Modifica
        fetch(`/app_cucina/schede/piatti/info/${schedaId}/${piattoId}`)
            .then(response => response.json())
            .then(data => {
                piattoIdInput.value = piattoId;
                form.elements['piatti'].value = data.piatti || '';
                form.elements['note'].value = data.note || '';
                form.elements['ordinatore'].value = data.ordinatore || '';
                modalTitle.textContent = 'Modifica Piatto';
                form.action = `/app_cucina/schede/piatti/info/${schedaId}/${piattoId}?servizio=${servizioId}`;  // Set the URL for PUT request
                submitButton.value = 'Aggiorna';
            })
            .catch(error => console.error('Errore:', error));
    } else {
        // Aggiungi
        piattoIdInput.value = '';
        form.reset();
        modalTitle.textContent = 'Aggiungi Nuovo Piatto';
        form.action = `/app_cucina/schede/piatti/${schedaId}?servizio=${servizioId}`;  // Corretto
        submitButton.value = 'Aggiungi';
    }

    modal.style.display = 'block';
}


function closePiattoModal() {
    document.getElementById('piattoModal').style.display = 'none';
}

function showCustomConfirmationModal(piattoId) {
    currentPiattoId = piattoId;
    document.getElementById('customConfirmationModal').style.display = 'block';
}

function closeCustomConfirmationModal() {
    document.getElementById('customConfirmationModal').style.display = 'none';
}

function handleCustomAction(action) {
    const url = `/app_cucina/schede/piatti/info/${schedaId}/${currentPiattoId}`;
    const method = action === 'delete' ? 'DELETE' : 'PUT';
    
    fetch(url, {
        method: method,
        headers: {
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert("Errore nell'operazione.");
        }
    }).catch(error => console.error('Errore:', error));

    closeCustomConfirmationModal();
}



window.onclick = function(event) {
    const piattoModal = document.getElementById("piattoModal");
    const confirmationModal = document.getElementById("customConfirmationModal");
    
    if (event.target === piattoModal) {
        closePiattoModal();
    }
    
    if (event.target === confirmationModal) {
        closeCustomConfirmationModal();
    }
}