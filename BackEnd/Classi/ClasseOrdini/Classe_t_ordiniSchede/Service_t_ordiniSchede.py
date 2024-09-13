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
    
    def check_letto(self, fkOrdine, fkReparto, data, fkServizio, fkScheda, letto):
        return self.repository.check_letto(fkOrdine, fkReparto, data, fkServizio, fkScheda, letto)

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
