from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Repository_t_preparazioniContenuti import Repository_t_preparazionicontenuti

class Service_t_preparazionicontenuti:

    def __init__(self):
        self.repository = Repository_t_preparazionicontenuti()

    def get_all_preparazioni_contenuti(self):
        return self.repository.get_all_preparazioni_contenuti()

    def get_preparazioni_contenuti_by_id(self, id):
        return self.repository.get_preparazioni_contenuti_by_id(id)

    def create_preparazioni_contenuti(self, fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None):
        return self.repository.create_preparazioni_contenuti(
            fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )
    
    def update_preparazioni_contenuti(self, id: int, fkPreparazione: int, fkAlimento: int, quantita: float,
                                      fkTipoQuantita: int, note: str, dataInserimento=None,
                                      utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None):
        return self.repository.update_preparazioni_contenuti(
            id, fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )

    def delete_preparazioni_contenuti(self, id):
        return self.repository.delete_preparazioni_contenuti(id)
