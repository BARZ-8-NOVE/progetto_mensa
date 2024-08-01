from datetime import datetime
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Repository_t_menuServiziAssociazione import RepositoryMenuServiziAssociazion

class Service_t_MenuServiziAssociazione:
    def __init__(self):
        self.repository = RepositoryMenuServiziAssociazion()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_by_fk_menu_servizio(self, fkMenuServizio):
        return self.repository.get_by_fk_menu_servizio(fkMenuServizio)

    def create(self, fkMenuServizio, fkAssociazione, utenteInserimento):

        return self.repository.create(fkMenuServizio, fkAssociazione, utenteInserimento)

    def update(self, id, fkMenuServizio, fkAssociazione, dataInserimento, utenteInserimento, dataCancellazione=None, utenteCancellazione=None):
        if dataCancellazione is None:
            dataCancellazione = datetime.now()
        if utenteCancellazione is None:
            utenteCancellazione = utenteInserimento
        return self.repository.update(id, fkMenuServizio, fkAssociazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)
    
    def delete_per_menu(self, fkMenuServizio, utenteCancellazione):
        return self.repository.delete_per_menu(fkMenuServizio, utenteCancellazione)
    
    def get_all_by_associazione_ids(self, fkMenuServizio):
        return self.repository.get_all_by_associazione_ids(fkMenuServizio)
    
    def populate_from_csv(self, csv_file):
        return self.repository.populate_from_csv(csv_file)
    
    def close(self):
        return self.repository.session.close()

