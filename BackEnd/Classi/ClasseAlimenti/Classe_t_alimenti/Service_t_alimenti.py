from Classi.ClasseAlimenti.Classe_t_alimenti.Repository_t_alimenti import RepositoryAlimenti
from Classi.ClasseUtility.UtilitiAlimenti.UtilityAlimenti import UtilityAlimenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Service_t_Alimenti:

    def __init__(self) -> None:
        self.repository = RepositoryAlimenti()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento):
        return self.repository.create(alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento)

    def update(self, id, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento):
        return self.repository.update(id, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento)

    def delete(self, id):
        return self.repository.delete(id)
    
    def get_alimento_by_name(self, name):
        UtilityAlimenti.check_nome_alimento(name)
        name = str(name)
        return self.repository.get_alimento_by_name(name.upper())
    
    def get_alimenti_by_tipologia_alimento(self, tipologia_alimento):
        UtilityGeneral.safe_int_convertion(tipologia_alimento, 'tipologia alimento')
        return self.repository.get_alimenti_by_tipologia_alimento(tipologia_alimento)