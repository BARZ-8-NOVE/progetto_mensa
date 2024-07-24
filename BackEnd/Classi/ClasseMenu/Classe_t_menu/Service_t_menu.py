from Classi.ClasseMenu.Classe_t_menu.Repository_t_menu import RepositoryMenu
from datetime import datetime

class ServiceMenu:

    def __init__(self) -> None:
        self.repository = RepositoryMenu()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, data, fkTipoMenu, dataInserimento, utenteInserimento):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.create(data, fkTipoMenu, dataInserimento, utenteInserimento)

    def update(self, id, data, fkTipoMenu, dataInserimento, utenteInserimento ):
        if not dataInserimento:
            dataInserimento = datetime.now()
        return self.repository.update(id, data, fkTipoMenu, dataInserimento, utenteInserimento)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)

    def get_by_month(self, year: int, month: int, tipo_menu: int = None):
        """
        Recupera i menu per il mese e l'anno specificati.
        
        :param year: Anno per cui recuperare i menu
        :param month: Mese per cui recuperare i menu
        :param tipo_menu: (Opzionale) Tipo di menu per filtrare i risultati
        :return: Lista di menu filtrati
        """
        return self.repository.get_by_mese_corrente(year, month, tipo_menu)
    
    def get_menu_details(self, year: int, month: int, tipo_menu: int = None, id_menu: int = None):
        return self.repository.get_menu_details( year, month, tipo_menu, id_menu)


   