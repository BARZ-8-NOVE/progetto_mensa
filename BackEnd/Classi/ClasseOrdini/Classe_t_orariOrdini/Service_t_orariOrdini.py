from Classi.ClasseOrdini.Classe_t_orariOrdini.Repository_t_orariOrdini import RepositoryOrariOrdini
from datetime import datetime

class Service_t_OrariOrdini:
    def __init__(self):
        self.repository = RepositoryOrariOrdini()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def update(self, id, nomeOrdine, fkServizio, tempoLimite, ordineDipendente, ordinePerOggi, utenteModifica):     
        return self.repository.update(id, nomeOrdine, fkServizio, tempoLimite,ordineDipendente, ordinePerOggi, utenteModifica)


    def check_order_time_limit(self, servizio, tipo_commensale, order_date):
        return self.repository.check_order_time_limit(servizio, tipo_commensale, order_date)
