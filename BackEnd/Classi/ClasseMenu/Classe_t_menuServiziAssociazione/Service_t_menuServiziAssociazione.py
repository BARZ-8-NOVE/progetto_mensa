from datetime import datetime
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Repository_t_menuServiziAssociazione import RepositoryMenuServiziAssociazion

class MenuServiziAssociazioneService:
    def __init__(self):
        self.repository = RepositoryMenuServiziAssociazion()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_by_fk_menu_servizio(self, fkMenuServizio):
        return self.repository.get_by_fk_menu_servizio(fkMenuServizio)

    def create(self, fkMenuServizio, fkAssociazione, utenteInserimento, dataInserimento=None):
        if dataInserimento is None:
            dataInserimento = datetime.now()
        return self.repository.create(fkMenuServizio, fkAssociazione, utenteInserimento, dataInserimento)

    def update(self, id, fkMenuServizio, fkAssociazione, dataInserimento, utenteInserimento, dataCancellazione=None, utenteCancellazione=None):
        if dataCancellazione is None:
            dataCancellazione = datetime.now()
        if utenteCancellazione is None:
            utenteCancellazione = utenteInserimento
        return self.repository.update(id, fkMenuServizio, fkAssociazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def get_all_by_associazione_ids(self, fkMenuServizio):
        return self.repository.get_all_by_associazione_ids(fkMenuServizio)

