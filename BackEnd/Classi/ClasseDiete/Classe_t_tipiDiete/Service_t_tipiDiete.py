from Classi.ClasseDiete.Classe_t_tipiDiete.Repository_t_tipiDiete import RepositoryTipiDiete

class Service_t_RepositoryTipiDiete:

    def __init__(self) -> None:
        self.repository = RepositoryTipiDiete()

    def get_all(self):
        return self.repository.get_all()