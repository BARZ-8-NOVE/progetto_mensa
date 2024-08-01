from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Repository_t_associazionePiattiPreparazioni import RepositoryAssociazionePiattiPreparazioni
from datetime import datetime
class Service_t_AssociazionePiattiPreparazionie:

    def __init__(self) -> None:
        self.repository = RepositoryAssociazionePiattiPreparazioni()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_by_id_ritorno_diz(self, id):
        return self.repository.get_by_id_ritorno_diz(id)    
    
    
    def create(self, fkPiatto, fkPreparazione, utenteInserimento , dataInserimento = None):

        return self.repository.create(fkPiatto, fkPreparazione, utenteInserimento, dataInserimento)

    def update(self, id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):

        return self.repository.update(id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def get_preparazione_by_piatto(self, fkPiatto):
        return self.repository.get_preparazione_by_piatto(fkPiatto)
    
    def get_id_by_preparazione_e_piatto(self, fkPiatto, fkpreparazione):
        return self.repository.get_id_by_preparazione_e_piatto(fkPiatto, fkpreparazione)
    
    

