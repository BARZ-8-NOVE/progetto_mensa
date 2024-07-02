from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
from datetime import datetime

class RepositoryOrdini:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TOrdini).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'fkReparto': result.fkReparto, 'data': result.data, 
                 'fkServizio': result.fkServizio, 'cognome': result.cognome, 'nome': result.nome, 
                 'letto': result.letto, 'dataInserimento': result.dataInserimento, 
                 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 
                 'utenteCancellazione': result.utenteCancellazione} for result in results]

    def get_by_id(self, id):
        try:
            result = self.session.query(TOrdini).filter_by(id=id).first()
        except Exception as e:
            return {'Error': str(e)}, 400
        if result:
            return {'id': result.id, 'fkReparto': result.fkReparto, 'data': result.data, 
                    'fkServizio': result.fkServizio, 'cognome': result.cognome, 'nome': result.nome, 
                    'letto': result.letto, 'dataInserimento': result.dataInserimento, 
                    'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 
                    'utenteCancellazione': result.utenteCancellazione}
        else:
            return {'Error': f'No match found for this id: {id}'}, 404

    def create(self, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento):
        try:
            ordine = TOrdini(
                fkReparto=fkReparto, 
                data=data, 
                fkServizio=fkServizio, 
                cognome=cognome, 
                nome=nome, 
                letto=letto, 
                dataInserimento=dataInserimento, 
                utenteInserimento=utenteInserimento
            )
            self.session.add(ordine)
            self.session.commit()
            return {'ordine': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def update(self, id, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento):
        try:
            ordine = self.session.query(TOrdini).filter_by(id=id).first()
            if ordine:
                ordine.fkReparto = fkReparto
                ordine.data = data
                ordine.fkServizio = fkServizio
                ordine.cognome = cognome
                ordine.nome = nome
                ordine.letto = letto
                ordine.dataInserimento = dataInserimento
                ordine.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'ordine': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete(self, id, utenteCancellazione):
        try:
            ordine = self.session.query(TOrdini).filter_by(id=id).first()
            if ordine:
                ordine.dataCancellazione = datetime.now()
                ordine.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'ordine': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
