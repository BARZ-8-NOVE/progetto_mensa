from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Domain_t_ordiniPiatti import TOrdiniPiatti
from Classi.ClasseOrdini.Classe_t_ordiniSchede.Domain_t_ordiniSchede import TOrdiniSchede
from datetime import datetime
from sqlalchemy.sql import func

class RepositoryOrdiniPiatti:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TOrdiniPiatti).all()
            return [{'id': result.id, 'fkOrdineScheda': result.fkOrdineScheda, 
                     'fkPiatto': result.fkPiatto, 'quantita': result.quantita, 
                     'note': result.note} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def get_all_by_ordine_scheda(self, fkOrdineScheda):
        try:
            results = self.session.query(TOrdiniPiatti).filter_by(fkOrdineScheda=fkOrdineScheda).all()
            return [{'id': result.id, 
                     'fkOrdineScheda': result.fkOrdineScheda, 
                     'fkPiatto': result.fkPiatto, 
                     'quantita': result.quantita, 
                     'note': result.note} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def get_by_id(self, id):
        try:
            result = self.session.query(TOrdiniPiatti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 
                        'fkOrdineScheda': result.fkOrdineScheda, 
                        'fkPiatto': result.fkPiatto, 
                        'quantita': result.quantita, 
                        'note': result.note}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def create(self, fkOrdineScheda, fkPiatto, quantita, note):
        try:
            ordine_piatto = TOrdiniPiatti(fkOrdineScheda=fkOrdineScheda, 
                                           fkPiatto=fkPiatto, 
                                           quantita=quantita, 
                                           note=note)
            self.session.add(ordine_piatto)
            self.session.commit()
            return {'ordine_piatto': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def update(self, id, fkOrdineScheda, fkPiatto, quantita, note):
        try:
            ordine_piatto = self.session.query(TOrdiniPiatti).filter_by(id=id).first()
            if ordine_piatto:
                ordine_piatto.fkOrdineScheda = fkOrdineScheda
                ordine_piatto.fkPiatto = fkPiatto
                ordine_piatto.quantita = quantita
                ordine_piatto.note = note
                self.session.commit()
                return {'ordine_piatto': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def delete(self, id):
        try:
            ordine_piatto = self.session.query(TOrdiniPiatti).filter_by(id=id).first()
            if ordine_piatto:
                self.session.delete(ordine_piatto)
                self.session.commit()
                return {'ordine_piatto': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def delete_by_fkOrdine(self, fkOrdineScheda):
        try:
            ordine_piatto = self.session.query(TOrdiniPiatti).filter_by(fkOrdineScheda=fkOrdineScheda).all()
            if ordine_piatto:
                for record in ordine_piatto:
                    self.session.delete(record)
                self.session.commit()
                return {'ordine_piatto': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for fkOrdineScheda: {fkOrdineScheda}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()

    def get_count_piatti(self, data, servizio: int, fkReparto=None, fkScheda=None):
        """Conta tutti i piatti da TOrdiniPiatti per un giorno specifico e che non sono stati cancellati."""
        try:
            query = self.session.query(
                TOrdiniSchede.fkReparto,
                TOrdiniPiatti.fkPiatto,
                func.sum(TOrdiniPiatti.quantita).label('piatti_count')
            ).join(
                TOrdiniSchede,
                TOrdiniPiatti.fkOrdineScheda == TOrdiniSchede.id
            ).filter(
                TOrdiniSchede.data == data,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            )

            if fkReparto is not None:
                query = query.filter(TOrdiniSchede.fkReparto == fkReparto)

            if fkScheda is not None:
                query = query.filter(TOrdiniSchede.fkScheda == fkScheda)

            results = query.group_by(TOrdiniSchede.fkReparto, TOrdiniPiatti.fkPiatto).all()

            # Organizza i risultati in un dizionario per facile accesso
            piatti_count = {}
            for result in results:
                if result.fkReparto not in piatti_count:
                    piatti_count[result.fkReparto] = {}
                piatti_count[result.fkReparto][result.fkPiatto] = result.piatti_count

            return piatti_count
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()
