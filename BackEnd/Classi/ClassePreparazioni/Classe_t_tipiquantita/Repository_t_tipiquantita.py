from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Domain_t_tipiquantita import TTipoQuantita

class Repository_t_tipoquantita:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_tipoquantita(self):
        try:
            results = self.session.query(TTipoQuantita).all()
            return [{'id': result.id, 'tipo': result.tipo, 'peso_valore_in_grammi': result.peso_valore_in_grammi, 'peso_valore_in_Kg': result.peso_valore_in_Kg} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_tipoquantita_by_id(self, id):
        try:
            result = self.session.query(TTipoQuantita).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'tipo': result.tipo, 'peso_valore_in_grammi': result.peso_valore_in_grammi, 'peso_valore_in_Kg': result.peso_valore_in_Kg}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()
            

    def create_tipoquantita(self, tipo, peso_valore_in_grammi=None, peso_valore_in_Kg=None):
        try:
            tipoquantita = TTipoQuantita(tipo=tipo, peso_valore_in_grammi=peso_valore_in_grammi, peso_valore_in_Kg=peso_valore_in_Kg)
            self.session.add(tipoquantita)
            self.session.commit()
            return {'tipoquantita': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

        
    def update_tipoquantita(self, id, tipo, peso_valore_in_grammi=None, peso_valore_in_Kg=None):
        try:
            tipoquantita = self.session.query(TTipoQuantita).filter_by(id=id).first()
            if tipoquantita:
                tipoquantita.tipo = tipo
                tipoquantita.peso_valore_in_grammi = peso_valore_in_grammi
                tipoquantita.peso_valore_in_Kg = peso_valore_in_Kg

                self.session.commit()
                return {'tipoquantita': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete_tipoquantita(self, id):
        try:
            tipoquantita = self.session.query(TTipoQuantita).filter_by(id=id).first()
            if tipoquantita:
                self.session.delete(tipoquantita)
                self.session.commit()
                return {'tipoquantita': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def transform_tipoquantita_g(self, quantita, id):
        try:
            # Recupera il record dal database
            result = self.session.query(TTipoQuantita).filter_by(id=id).first()
            
            if result:
                if result.peso_valore_in_grammi is not None: 
                    # Se è disponibile il valore in grammi, calcola la nuova quantità
                    nuova_quantita = quantita * result.peso_valore_in_grammi
                    return { 
                        'quantita_in_g': nuova_quantita,
                        'id': 1
                    }
                else: 
                    # Se non è disponibile una trasformazione, restituisci la quantità originale
                    return { 
                        'trasformazione_non_disponibile': quantita,
                        'id': id
                    }
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        
        except Exception as e:
            # In caso di errore, esegui il rollback della transazione
            self.session.rollback()
            return {'Error': str(e)}, 400
        
        finally:
            # Chiudi la sessione solo se non è gestita da qualche altra parte
            if not self.session.is_active:
                self.session.close()


    def transform_tipoquantita_kg(self, quantita, id):
        try:
            # Recupera il record dal database
            result = self.session.query(TTipoQuantita).filter_by(id=id).first()
            
            if result:
                if result.peso_valore_in_grammi is not None: 
                    # Se è disponibile il valore in grammi, calcola la nuova quantità
                    nuova_quantita = quantita * result.peso_valore_in_Kg
                    return { 
                        'quantita_in_kg': nuova_quantita,
                        'id': 3
                    }
                else: 
                    # Se non è disponibile una trasformazione, restituisci la quantità originale
                    return { 
                        'trasformazione_non_disponibile': quantita,
                        'id': id
                    }
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        
        except Exception as e:
            # In caso di errore, esegui il rollback della transazione
            self.session.rollback()
            return {'Error': str(e)}, 400
        
        finally:
            # Chiudi la sessione solo se non è gestita da qualche altra parte
            if not self.session.is_active:
                self.session.close()
