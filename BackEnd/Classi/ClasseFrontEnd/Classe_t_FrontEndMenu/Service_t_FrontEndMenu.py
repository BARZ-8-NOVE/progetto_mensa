from Classi.ClasseFrontEnd.Classe_t_FrontEndMenu.Repository_t_FrontEndMenu import RepositoryTFrontEndMenu

class TFrontEndMenuService:
    def __init__(self):
        self.repository = RepositoryTFrontEndMenu()

    def get_all_menus(self):
        return self.repository.get_all()

    def get_menu_by_id(self, menu_id):
        return self.repository.get_by_id(menu_id)
