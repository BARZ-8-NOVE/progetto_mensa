from Classi.ClasseFrontEnd.Classe_t_FrontEndVociFiglieMenu.Repository_t_FrontEndVociFiglieMenu import RepositoryTFrontEndVociFiglieMenu
class TFrontEndMenuVociFiglieService:
    def __init__(self):
        self.repository = RepositoryTFrontEndVociFiglieMenu()

    def get_all_menus(self):
        return self.repository.get_all()

    def get_menu_by_id(self, menu_id):
        return self.repository.get_by_id(menu_id)
