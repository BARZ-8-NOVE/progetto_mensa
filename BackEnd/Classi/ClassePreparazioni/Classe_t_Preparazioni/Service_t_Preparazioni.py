from Classi.ClassePreparazioni.Classe_t_Preparazioni.Repository_t_Preparazioni import Repository_t_preparazioni

class Service_t_preparazioni:

    def __init__(self):
        self.repository = Repository_t_preparazioni()

    def get_all_preparazioni(self):
        return self.repository.get_all_preparazioni()

    def get_preparazione_by_id(self, id):
        return self.repository.get_preparazione_by_id(id)
    
    def get_all_preparazioni_base(self):
        return self.repository.get_all_preparazioni_base()

    def update(self, id, fkTipoPreparazione, descrizione, isEstivo, isInvernale, inizio, fine, immagine):
        return self.repository.update(id, fkTipoPreparazione, descrizione, isEstivo, isInvernale, inizio, fine, immagine)

    
    def get_descrizione_by_id(self, id):
        return self.repository.get_descrizione_by_id(id)

    def create_preparazione(self, fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni=None, inizio=None, fine=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None, immagine=None):
        return self.repository.create_preparazione(
            fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni, inizio, fine,
            dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione, immagine
        )
    
    def get_last_id(self):
        return self.repository.get_last_id()

    def delete_preparazione(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def calcola_calorie_per_nome(self, titolo_piatto):
        return self.repository.calcola_calorie_per_nome(titolo_piatto)
    
    def recupero_totale_ingredienti_base(self, descrizione):
        return self.repository.recupero_totale_ingredienti_base(descrizione)
    
    def recupero_totale_peso_ingredienti(self, descrizione):
        return self.repository.recupero_totale_peso_ingredienti(descrizione)

