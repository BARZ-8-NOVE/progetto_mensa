// Funzione per mostrare una sezione specifica
function showSection(sectionId) {
    // Nascondi tutte le sezioni
    document.querySelectorAll('.menu-section').forEach(section => {
        section.style.display = 'none';
    });

    // Mostra la sezione selezionata
    document.getElementById(sectionId).style.display = 'block';
}

// Chiama showSection per mostrare la sezione iniziale





function updatePreparazioni() {
    console.log('Updating preparazioni visibility...');
    
    // Trova tutti i piatti selezionati
    const selectedPiatti = Array.from(document.querySelectorAll('input[name="piatti"]:checked')).map(cb => parseInt(cb.value));
    console.log('Selected Piatti:', selectedPiatti);

    // Mostra i contenitori per i piatti selezionati e nascondi quelli non selezionati
    document.querySelectorAll('div[id^="preparazioni-container-"]').forEach(container => {
        const piattoId = container.id.split('-')[2];
        if (selectedPiatti.includes(parseInt(piattoId))) {
            container.style.display = 'block'; // Mostra il contenitore per i piatti selezionati
        } else {
            container.style.display = 'none'; // Nascondi i contenitori per i piatti non selezionati
        }
    });
}

// Associa l'evento change ai checkbox
document.querySelectorAll('input[name="piatti"]').forEach(checkbox => {
    checkbox.addEventListener('change', updatePreparazioni);
});

// Chiama updatePreparazioni al caricamento della pagina per visualizzare i contenitori appropriati
updatePreparazioni();



