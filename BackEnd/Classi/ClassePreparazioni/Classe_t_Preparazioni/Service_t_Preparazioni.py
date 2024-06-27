from Classi.ClassePreparazioni.Classe_t_Preparazioni.Repository_t_Preparazioni import Repository_t_preparazioni

class Service_t_preparazioni:

    def __init__(self):
        self.repository = Repository_t_preparazioni()

    def get_all_preparazioni(self):
        return self.repository.get_all_preparazioni()

    def get_preparazione_by_id(self, id):
        return self.repository.get_preparazione_by_id(id)

    def create_preparazione(self, fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni=None, inizio=None, fine=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None, immagine=None):
        return self.repository.create_preparazione(
            fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni, inizio, fine,
            dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione, immagine
        )

    def delete_preparazione(self, id):
        return self.repository.delete_preparazione(id)
