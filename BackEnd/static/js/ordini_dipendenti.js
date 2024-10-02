
    

    function printProspetto(ordineId) {
        // Costruisci l'URL per la pagina di stampa
        var url = '/app_cucina/ordini/printProspetto/' + ordineId;
    
        // Apri una nuova finestra con la pagina di stampa
        var printWindow = window.open(url, '_blank', 'width=800,height=600');
        
        // Attendere che la finestra venga caricata
        printWindow.onload = function() {
            printWindow.print();
        };
    }



    function showForm(ordineId, servizioId, repartoId, schedaId) {
        const url = `ordini/schede_dipendenti/${ordineId}/${servizioId}/${repartoId}/${schedaId}`;
        console.log("Redirecting to URL: " + url);  // Aggiungi questo per vedere l'URL generato
        window.location.href = url;
    }
    
    function printPage(ordineId) {
        // Costruisci l'URL per la pagina di stampa
        var url = '/app_cucina/ordini/print/' + ordineId;
    
        // Apri una nuova finestra con la pagina di stampa
        var printWindow = window.open(url, '_blank', 'width=800,height=600');
        
        // Attendere che la finestra venga caricata
        printWindow.onload = function() {
            printWindow.print();
        };
    }