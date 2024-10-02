function showForm() {
    document.getElementById('passwordModal').style.display = 'block';
}

function closeForm() {
    document.getElementById('passwordModal').style.display = 'none';
}

// Chiudi il popup se l'utente clicca al di fuori del contenuto del popup
window.onclick = function(event) {
    if (event.target == document.getElementById('passwordModal')) {
        closeForm();
    }
}

function showFormEmail() {
    document.getElementById('emailModal').style.display = 'block';
}

function closeFormEmail() {
    document.getElementById('emailModal').style.display = 'none';
}

// Chiudi il popup se l'utente clicca al di fuori del contenuto del popup
window.onclick = function(event) {
    if (event.target == document.getElementById('emailModal')) {
        closeFormEmail();
    }
}