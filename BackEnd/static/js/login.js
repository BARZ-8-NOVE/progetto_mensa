 // Script per la gestione del popup
 var modal = document.getElementById("forgotPasswordModal");
 var btn = document.getElementById("forgotPasswordBtn");
 var span = document.getElementsByClassName("close")[0];

 // Quando si clicca sul bottone "Password Dimenticata", mostra il popup
 btn.onclick = function() {
     modal.style.display = "block";
 }

 // Quando si clicca sulla X, chiudi il popup
 span.onclick = function() {
     modal.style.display = "none";
 }

 // Quando si clicca fuori dal popup, chiudi il popup
 window.onclick = function(event) {
     if (event.target == modal) {
         modal.style.display = "none";
     }
 }