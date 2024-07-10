from Classi.ClasseFrontEnd.Classe_t_FrontEndVociMenu.Repository_t_FrontEndVociMenu import RepositoryTFrontEndVociMenu
class TFrontEndMenuVociService:
    def __init__(self):
        self.repository = RepositoryTFrontEndVociMenu()

    def get_all_menus(self):
        return self.repository.get_all()

    def get_menu_by_id(self, menu_id):
        return self.repository.get_by_id(menu_id)
    
    def get_all_children(self, menu_id):
        return self.repository.get_all_by_fkFrontEndMenu(menu_id)
