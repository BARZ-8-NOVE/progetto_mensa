from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Repository_t_associazionePiattiPreparazioni import RepositoryAssociazionePiattiPreparazioni
from datetime import datetime
class ServiceAssociazionePiattiPreparazionie:

    def __init__(self) -> None:
        self.repository = RepositoryAssociazionePiattiPreparazioni()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(fkPiatto, fkPreparazione, dataInserimento, utenteInserimento)

    def update(self, id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.update(id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
