from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Domain_t_ordiniPiatti import TOrdiniPiatti

class RepositoryOrdiniPiatti:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TOrdiniPiatti).all()
            return [{'id': result.id, 'fkOrdineScheda': result.fkOrdineScheda, 'fkPiatto': result.fkPiatto, 'quantita': result.quantita, 'note': result.note} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()
        

    def get_all_by_ordine_scheda(self, fkOrdineScheda):
        try:
            results = self.session.query(TOrdiniPiatti).filter_by(fkOrdineScheda=fkOrdineScheda).all()
            return [{'id': result.id, 'fkOrdineScheda': result.fkOrdineScheda, 'fkPiatto': result.fkPiatto, 'quantita': result.quantita, 'note': result.note} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()



    def get_by_id(self, id):
        try:
            result = self.session.query(TOrdiniPiatti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'fkOrdineScheda': result.fkOrdineScheda, 'fkPiatto': result.fkPiatto, 'quantita': result.quantita, 'note': result.note}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 500
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()

    def create(self, fkOrdineScheda, fkPiatto, quantita, note):
        try:
            ordine_piatto = TOrdiniPiatti(fkOrdineScheda=fkOrdineScheda, fkPiatto=fkPiatto, quantita=quantita, note=note)
            self.session.add(ordine_piatto)
            self.session.commit()
            return {'ordine_piatto': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
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
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
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
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()
        

    def delete_by_fkOrdine(self, fkOrdineScheda):
        try:
            # Trova tutti i record associati a fkOrdineScheda
            ordine_piatto = self.session.query(TOrdiniPiatti).filter_by(fkOrdineScheda=fkOrdineScheda).all()
            
            if ordine_piatto:
                # Elimina ogni record trovato
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
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()
