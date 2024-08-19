from Classi.ClasseDiete.Classe_t_tipiAlimentazione.Repository_t_tipiAlimentazione import RepositoryTipiAlimentazione

class Service_t_TipiAlimentazione:

    def __init__(self) -> None:
        self.repository = RepositoryTipiAlimentazione()

    def get_all(self):
        return self.repository.get_all()