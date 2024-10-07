from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAlimenti.Classe_t_alimenti.Domani_t_alimenti import TAlimenti
import logging
from werkzeug.exceptions import NotFound

class RepositoryAlimenti:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TAlimenti).order_by(TAlimenti.alimento).all()
            return [{'id': result.id, 'alimento': result.alimento, 'energia_Kcal': result.energia_Kcal, 
                     'energia_KJ': result.energia_KJ, 'prot_tot_gr': result.prot_tot_gr, 
                     'glucidi_tot': result.glucidi_tot, 'lipidi_tot': result.lipidi_tot, 
                     'saturi_tot': result.saturi_tot, 'fkAllergene': result.fkAllergene, 
                     'fkTipologiaAlimento': result.fkTipologiaAlimento} for result in results]
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting all alimenti: {e}")
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()

    def get_by_id(self, id):
        try:
            result = self.session.query(TAlimenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'alimento': result.alimento, 'energia_Kcal': result.energia_Kcal, 
                        'energia_KJ': result.energia_KJ, 'prot_tot_gr': result.prot_tot_gr, 
                        'glucidi_tot': result.glucidi_tot, 'lipidi_tot': result.lipidi_tot, 
                        'saturi_tot': result.saturi_tot, 'fkAllergene': result.fkAllergene, 
                        'fkTipologiaAlimento': result.fkTipologiaAlimento}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            if self.session:
                self.session.close()
        
    def get_alimento_by_name(self, name):
        try:
            result = self.session.query(TAlimenti).filter(TAlimenti.alimento.ilike(f'%{name}%')).all()
            if result:
                return [{'id': r.id, 'alimento': r.alimento} for r in result]  # Restituisci i risultati in un formato standard
            else:
                raise NotFound(f'Cannot find alimento for this name: {name}')
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting alimento by name {name}: {e}")
            raise NotFound(f'Error: {str(e)}')
        finally:
            if self.session:
                self.session.close()

    def get_alimenti_by_tipologia_alimento(self, tipologia_alimento):
        try:
            result = self.session.query(TAlimenti).filter_by(fkTipologiaAlimento=tipologia_alimento).all()
            if result:
                return [{'id': r.id, 'alimento': r.alimento} for r in result]  # Restituisci i risultati in un formato standard
            else:
                raise NotFound(f'Cannot find alimenti for this tipologia: {tipologia_alimento}')
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting alimenti by tipologia {tipologia_alimento}: {e}")
            raise NotFound(f'Error: {str(e)}')
        finally:
            if self.session:
                self.session.close()

    def create(self, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento):
        try:
            new_alimento = TAlimenti(
                alimento=alimento,
                energia_Kcal=energia_Kcal,
                energia_KJ=energia_KJ,
                prot_tot_gr=prot_tot_gr,
                glucidi_tot=glucidi_tot,
                lipidi_tot=lipidi_tot,
                saturi_tot=saturi_tot,
                fkAllergene=fkAllergene,
                fkTipologiaAlimento=fkTipologiaAlimento
            )
            self.session.add(new_alimento)
            self.session.commit()
            return {'alimento': 'added!'}, 200
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error creating alimento: {e}")
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()

    def update(self, id, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento):
        try:
            alim = self.session.query(TAlimenti).filter_by(id=id).first()
            if alimento:
  
                alim.alimento = alimento
                alim.energia_Kcal = energia_Kcal
                alim.energia_KJ = energia_KJ
                alim.prot_tot_gr = prot_tot_gr
                alim.glucidi_tot = glucidi_tot
                alim.lipidi_tot = lipidi_tot
                alim.saturi_tot = saturi_tot
                alim.fkAllergene = fkAllergene
                alim.fkTipologiaAlimento = fkTipologiaAlimento
                
                self.session.commit()
                print(f"Aggiornamento avvenuto con successo per ID {id}.")  # Stampa di successo
                return {'alimento': 'updated!', 'id': id}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating alimento with ID {id}: {e}")
            print(f"Errore durante l'aggiornamento: {e}")  # Stampa dell'errore
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()

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
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error deleting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()
