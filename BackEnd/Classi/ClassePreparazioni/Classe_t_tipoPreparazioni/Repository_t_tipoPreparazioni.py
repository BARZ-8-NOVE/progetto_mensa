from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Domain_t_tipoPreparazioni import TTipiPreparazioni

class Repository_t_tipipreparazioni:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_tipipreparazioni(self):
        try:
            results = self.session.query(TTipiPreparazioni).all()
            return [{'id': result.id, 'descrizione': result.descrizione} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def get_tipipreparazioni_by_id(self, id):
        try:
            result = self.session.query(TTipiPreparazioni).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'descrizione': result.descrizione}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def create_tipipreparazioni(self, descrizione):
        try:
            tipipreparazioni = TTipiPreparazioni(descrizione=descrizione)
            self.session.add(tipipreparazioni)
            self.session.commit()
            return {'tipipreparazioni': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()
        
    def update_tipipreparazioni(self, id, descrizione):
        try:
            tipipreparazioni = self.session.query(TTipiPreparazioni).filter_by(id=id).first()
            if tipipreparazioni:
                tipipreparazioni.descrizione = descrizione
                self.session.commit()
                return {'tipipreparazioni': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def delete_tipipreparazioni(self, id):
        try:
            tipipreparazioni = self.session.query(TTipiPreparazioni).filter_by(id=id).first()
            if tipipreparazioni:
                self.session.delete(tipipreparazioni)
                self.session.commit()
                return {'tipipreparazioni': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()
