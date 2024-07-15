document.addEventListener('DOMContentLoaded', function() {


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

    // Crea una mappa per le tipologie
    const searchTypeMap = {};
    {% for tipologia in tipologie %}
        searchTypeMap["{{ tipologia.id }}"] = "{{ tipologia.nome }}";
    {% endfor %}

    // Event listener per i filtri
    searchNameInput.addEventListener('input', filterTable);
    searchTypeSelect.addEventListener('change', filterTable);
});