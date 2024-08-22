from Classi.ClasseUtenti.Classe_t_funzionalita.Repository_t_funzionalita import TFunzionalitaRepository


class Service_t_funzionalita:
    
    
    def __init__(self):
        self.repository = TFunzionalitaRepository()

    def get_all_menus(self):
        return self.repository.get_all()
    
    def get_menu_principale(self):
        return self.repository.get_menu_principale()

    def get_menu_by_id(self, menu_id):
        return self.repository.get_by_id(menu_id)
    
    def get_all_children(self, fkPadre):
        return self.repository.get_by_padre(fkPadre)
    
    def can_access(self, user_type_id, page_link):
        return self.repository.can_access(user_type_id, page_link)