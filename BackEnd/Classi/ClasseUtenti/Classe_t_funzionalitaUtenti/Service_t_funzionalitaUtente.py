from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Repository_t_funzionalitaUtente import TFunzionalitaUtenteRepository

class Service_t_FunzionalitaUtente:
    def __init__(self):
        self.repository = TFunzionalitaUtenteRepository()

    def get_funzionalita_utente_by_id(self, funzionalita_utente_id: int):
        return self.repository.get_funzionalita_utente_by_id(funzionalita_utente_id)

    def get_funzionalita_utenti_by_user_type(self, tipo_utente_id: int):
        return self.repository.get_funzionalita_utenti_by_user_type(tipo_utente_id)

    def get_funzionalita_utenti_by_funzionalita(self, funzionalita_id: int):
        return self.repository.get_funzionalita_utenti_by_funzionalita(funzionalita_id)

    def get_all_funzionalita_utenti(self):
        return self.repository.get_all_funzionalita_utenti()
    
    def build_menu_structure(self, user_id):
        data = self.repository.get_menu_data(user_id)
        
        menu_structure = []

        for item in data:
            if item.fkPadre is None:
                item_dict = {
                    'id': item.funzionalita_id,
                    'titolo': item.titolo,
                    'label': item.label,
                    'icon': item.icon,
                    'link': item.link,
                    'ordinatore': item.ordinatore,
                    'target': item.target,
                    'dataCancellazione': item.dataCancellazione,
                    'figli': [],
                    'nipoti': []
                }
                menu_structure.append(item_dict)

        for item in data:
            if item.fkPadre is not None:
                for padre in menu_structure:
                    if padre['id'] == item.fkPadre:
                        if item.funzionalita_id not in [figlio['id'] for figlio in padre['figli']]:
                            figlio_dict = {
                                'id': item.funzionalita_id,
                                'titolo': item.titolo,
                                'label': item.label,
                                'icon': item.icon,
                                'link': item.link,
                                'ordinatore': item.ordinatore,
                                'target': item.target,
                                'dataCancellazione': item.dataCancellazione,
                                'nipoti': []
                            }
                            padre['figli'].append(figlio_dict)
                        break

        for padre in menu_structure:
            for figlio in padre['figli']:
                for item in data:
                    if item.fkPadre == figlio['id']:
                        if item.funzionalita_id not in [nipote['id'] for nipote in figlio['nipoti']]:
                            nipote_dict = {
                                'id': item.funzionalita_id,
                                'titolo': item.titolo,
                                'label': item.label,
                                'icon': item.icon,
                                'link': item.link,
                                'ordinatore': item.ordinatore,
                                'target': item.target,
                                'dataCancellazione': item.dataCancellazione
                            }
                            figlio['nipoti'].append(nipote_dict)

        return menu_structure
    



    def get_funz_utenti_by_user_type(self, tipo_utente_id: int):
        return self.repository.get_funz_utenti_by_user_type(tipo_utente_id)
    

    def create(self, tipo_utente_id, fkFunzionalita, permessi ):
        return self.repository.create(tipo_utente_id, fkFunzionalita, permessi)
    
    def delete_by_tipo_utente(self, tipo_utente_id):
        return self.repository.delete_by_tipo_utente(tipo_utente_id)