from Classi.ClasseOrdini.Classe_t_ordiniSchede.Repository_t_ordiniSchede import RepositoryOrdiniSchede
from datetime import datetime

class Service_t_OrdiniSchede:
    def __init__(self):
        self.repository = RepositoryOrdiniSchede()

    def get_all_by_day(self, year: int, month: int, day: int, servizio: int):
        return self.repository.get_all_by_day(year, month, day, servizio)
    
    def get_all_by_ordine(self, ordine):
        return self.repository.get_all_by_ordine(ordine)
    
    def get_count_filtrati(self, year: int, month: int, day: int, servizio: int, fkReparto = None, fkScheda = None):
        return self.repository.get_count_filtrati(year, month, day, servizio, fkReparto, fkScheda)
    

    def count_brodi(self, data, fkOrdine: int):
        return self.repository.count_brodi(data, fkOrdine)
    
    # def get_all_filtrati(self, year: int, month: int, day: int, servizio: int):
    #     return self.repository.get_all_filtrati(year, month, day, servizio)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto, utenteInserimento):      
        return self.repository.create(fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto, utenteInserimento)

    def update(self, fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto, utenteInserimento):  
        return self.repository.update(id, fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def get_all_by_day_and_reparto(self, data, fkReparto, servizio, scheda):
         return self.repository.get_all_by_day_and_reparto(data, fkReparto, servizio, scheda)
    
    def check_letto(self, fkOrdine, fkReparto, data, fkServizio, letto):
        return self.repository.check_letto(fkOrdine, fkReparto, data, fkServizio, letto)
    
    def get_all_by_ordine_per_stampa(self, fkOrdine):
        return self.repository.get_all_by_ordine_per_stampa(fkOrdine)

    # services.py

    def get_ordini_data(self, year, month, day, servizio_corrente, reparti, schede_attive):
        schede_count = self.get_count_filtrati(year, month, day, servizio_corrente)
        reparti_totals = {reparto['id']: 0 for reparto in reparti}
        schede_totals = {scheda['id']: 0 for scheda in schede_attive}
        total_general = 0

        for reparto in reparti:
            reparto_id = reparto['id']
            for scheda in schede_attive:
                scheda_id = scheda['id']
                count = schede_count.get(reparto_id, {}).get(scheda_id, 0)
                reparti_totals[reparto_id] += count
                schede_totals[scheda_id] += count
                total_general += count

        return schede_count, reparti_totals, schede_totals, total_general
    

    def get_by_day_and_nome_cognome(self, data, nome: str, cognome: str, servizio: int):
        return self.repository.get_by_day_and_nome_cognome( data, nome, cognome, servizio)
    
    def count_totali_per_giorno(self, data, servizio: int):
        return self.repository.count_totali_per_giorno( data, servizio)



    def calcola_totali_per_giorno(self, data, servizi):
        ordini_totali_per_servizio = {}
        totale_pazienti = 0
        totale_personale = 0
        totale_completo = 0

        for servizio in servizi:
            ordini_totali = self.repository.count_totali_per_giorno(data, servizio['id'])
            servizio_nome = servizio['descrizione']
            ordini_totali_per_servizio[servizio_nome] = ordini_totali
            
            totale_pazienti += ordini_totali['totale_pazienti']
            totale_personale += ordini_totali['totale_personale']
            totale_completo += ordini_totali['totale_completo']

        return ordini_totali_per_servizio, totale_pazienti, totale_personale, totale_completo
    

    def count_totali_per_mese(self, mese: int, anno: int, servizio: int):
        """Conta i totali degli ordini per un mese specifico e un servizio."""
        return self.repository.count_totali_per_mese(mese, anno, servizio)

    def calcola_totali_per_mese(self, mese, anno, servizi):
        """Calcola i totali degli ordini per mese, divisi per servizio, e il totale complessivo."""
        ordini_totali_mese_per_servizio = {}
        totale_mese_completo = 0

        for servizio in servizi:
            # Ottieni il totale degli ordini per il servizio specifico
            ordini_totali = self.count_totali_per_mese(mese, anno, servizio['id'])
            servizio_nome = servizio['descrizione']

            # Aggiungi il totale per questo servizio al dizionario
            ordini_totali_mese_per_servizio[servizio_nome] = ordini_totali['totale_completo']
            
            # Somma il totale complessivo
            totale_mese_completo += ordini_totali['totale_completo']

        return ordini_totali_mese_per_servizio, totale_mese_completo


    def count_totali_per_anno(self, anno: int, servizio: int):
        """Conta i totali degli ordini per un anno specifico e un servizio."""
        return self.repository.count_totali_per_anno(anno, servizio)

    def calcola_totali_per_anno(self, anno, servizi):
        """Calcola i totali degli ordini per anno, divisi per servizio, e il totale complessivo."""
        ordini_totali_anno_per_servizio = {}
        totale_anno_completo = 0

        for servizio in servizi:
            # Ottieni il totale degli ordini per il servizio specifico
            ordini_totali = self.count_totali_per_anno(anno, servizio['id'])
            servizio_nome = servizio['descrizione']

            # Aggiungi il totale per questo servizio al dizionario
            ordini_totali_anno_per_servizio[servizio_nome] = ordini_totali['totale_completo']
            
            # Somma il totale complessivo
            totale_anno_completo += ordini_totali['totale_completo']

        return ordini_totali_anno_per_servizio, totale_anno_completo
    
    def count_totali_tipo_menu(self, anno: int, mese=None, giorno=None):
        return self.repository.count_totali_tipo_menu(anno, mese, giorno)