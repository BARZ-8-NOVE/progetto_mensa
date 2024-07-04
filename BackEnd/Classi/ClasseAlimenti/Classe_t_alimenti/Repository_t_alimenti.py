from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAlimenti.Classe_t_alimenti.Domani_t_alimenti import TAlimenti
import logging

class RepositoryAlimenti:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TAlimenti).all()
            return [{'id': result.id, 'Alimento': result.alimento, 'Energia_Kcal': result.energia_Kcal, 'Energia_KJ': result.energia_KJ, 'Prot_Tot_Gr': result.prot_tot_gr, 'Glucidi_Tot': result.glucidi_tot, 'Lipidi_Tot': result.lipidi_tot, 'Saturi_Tot': result.saturi_tot, 'fkAllergene': result.fkAllergene, 'fkTipologiaAlimento': result.fkTipologiaAlimento} for result in results]
        except Exception as e:
            logging.error(f"Error getting all alimenti: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TAlimenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'Alimento': result.alimento, 'Energia_Kcal': result.energia_Kcal, 'Energia_KJ': result.energia_KJ, 'Prot_Tot_Gr': result.prot_tot_gr, 'Glucidi_Tot': result.glucidi_tot, 'Lipidi_Tot': result.lipidi_tot, 'Saturi_Tot': result.saturi_tot, 'fkAllergene': result.fkAllergene, 'fkTipologiaAlimento': result.fkTipologiaAlimento}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 400
        
    def create(self, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento):
        try:
            alimento = TAlimenti(Alimento=Alimento, Energia_Kcal=Energia_Kcal, Energia_KJ=Energia_KJ, Prot_Tot_Gr=Prot_Tot_Gr, Glucidi_Tot=Glucidi_Tot, Lipidi_Tot=Lipidi_Tot, Saturi_Tot=Saturi_Tot, fkAllergene=fkAllergene, fkTipologiaAlimento=fkTipologiaAlimento)
            self.session.add(alimento)
            self.session.commit()
            return {'alimento': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating alimento: {e}")
            return {'Error': str(e)}, 500

    def update(self, id, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento):
        try:
            alimento = self.session.query(TAlimenti).filter_by(id=id).first()
            if alimento:
                alimento.alimento = Alimento
                alimento.energia_Kcal = Energia_Kcal
                alimento.energia_KJ = Energia_KJ
                alimento.prot_tot_gr = Prot_Tot_Gr
                alimento.glucidi_tot = Glucidi_Tot
                alimento.lipidi_tot = Lipidi_Tot
                alimento.saturi_tot = Saturi_Tot
                alimento.fkAllergene = fkAllergene
                alimento.fkTipologiaAlimento = fkTipologiaAlimento
                self.session.commit()
                return {'alimento': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating alimento with ID {id}: {e}")
            return {'Error': str(e)}, 500

    def delete(self, id):
        try:
            result = self.session.query(TAlimenti).filter_by(id=id).first()
            if result:
                self.session.delete(result)
                self.session.commit()
                return {'alimento': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 500
