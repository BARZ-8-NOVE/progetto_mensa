from Classi.ClasseSchede.Classe_t_schede.Repository_t_schede import RepositoryTSchede
from datetime import datetime
class Service_t_Schede:

    def __init__(self) -> None:
        self.repository = RepositoryTSchede()

    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_all_attivi_pazienti(self):
        return self.repository.get_all_attivi_pazienti()
    
    def get_all_personale(self):
        return self.repository.get_all_personale()
    
    def create(self, fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa):
        return self.repository.create(fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa)
    
    def update(self,id, fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa):
        return self.repository.update(id, fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa)

    def delete(self, id, utenteCancellazione):
        return self.repository.delete(id, utenteCancellazione)

    def serialize(self, scheda):
        return {
            'id': scheda.id,
            'backgroundColor': scheda.backgroundColor,
            'color': scheda.color,
            'fkTipoAlimentazione': scheda.fkTipoAlimentazione,
            'fkTipoMenu': scheda.fkTipoMenu,
            'fkSchedaPreconfezionata': scheda.fkSchedaPreconfezionata,
            'nome': scheda.nome,
            'titolo': scheda.titolo,
            'sottotitolo': scheda.sottotitolo,
            'descrizione': scheda.descrizione,
            'dipendente': scheda.dipendente,
            'nominativa': scheda.nominativa,
            'inizio': scheda.inizio.strftime('%Y-%m-%d') if scheda.inizio else None,
            'fine': scheda.fine.strftime('%Y-%m-%d') if scheda.fine else None,
            'note': scheda.note,
            'dataInserimento': scheda.dataInserimento.strftime('%Y-%m-%d %H:%M:%S') if scheda.dataInserimento else None,
            'utenteInserimento': scheda.utenteInserimento,
            'dataCancellazione': scheda.dataCancellazione.strftime('%Y-%m-%d %H:%M:%S') if scheda.dataCancellazione else None,
            'utenteCancellazione': scheda.utenteCancellazione
        }