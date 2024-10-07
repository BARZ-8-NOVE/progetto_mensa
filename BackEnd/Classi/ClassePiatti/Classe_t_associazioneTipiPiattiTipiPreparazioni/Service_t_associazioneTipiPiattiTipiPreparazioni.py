from Classe_t_associazioneTipiPiattiTipiPreparazioni.Repository_t_associazioneTipiPiattiTipiPreparazioni import RepositoryAssociazioneTipiPiattiTipiPreparazioni
from datetime import datetime

class Service_t_AssociazioneTipiPiattiTipiPreparazionie:

    def __init__(self) -> None:
        self.repository = RepositoryAssociazioneTipiPiattiTipiPreparazioni()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, fkPiatto, fkPreparazione, utenteInserimento , dataInserimento = None):

        return self.repository.create(fkPiatto, fkPreparazione, utenteInserimento, dataInserimento)

    def update(self, id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):

        return self.repository.update(id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def delete_associazione(self, fkPreparazione , utenteCancellazione):
        return self.repository.delete_associazione(fkPreparazione, utenteCancellazione)
    
    def get_tipoPreparazione_by_TipoPiatto(self, fkPiatto):
        return self.repository.get_tipoPreparazione_by_TipoPiatto(fkPiatto)
    
    def get_fkTipoPatto_by_fkTipoPeparazione(self, fkPreparazione):
        return self.repository.get_fkTipoPatto_by_fkTipoPeparazione(fkPreparazione)
    

    
    
