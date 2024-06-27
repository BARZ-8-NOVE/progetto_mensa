from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Repository_t_preparazioniContenuti import Repository_t_tipipreparazionicontenuti

class Service_t_tipipreparazionicontenuti:

    def __init__(self):
        self.repository = Repository_t_tipipreparazionicontenuti()

    def get_all_tipi_preparazioni_contenuti(self):
        return self.repository.get_all_tipi_preparazioni_contenuti()

    def get_tipi_preparazioni_contenuti_by_id(self, id):
        return self.repository.get_tipi_preparazioni_contenuti_by_id(id)

    def create_tipi_preparazioni_contenuti(self, fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None):
        return self.repository.create_tipi_preparazioni_contenuti(
            fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )

    def delete_tipi_preparazioni_contenuti(self, id):
        return self.repository.delete_tipi_preparazioni_contenuti(id)
