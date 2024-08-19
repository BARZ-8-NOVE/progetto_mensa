from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordiniSchede.Domain_t_ordiniSchede import TOrdiniSchede
from sqlalchemy.sql import func
from datetime import datetime

class RepositoryOrdiniSchede:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_by_day(self, year: int, month: int, day: int, servizio: int):
        """Recupera tutti i record da TOrdiniSchede per un giorno specifico e che non sono stati cancellati."""
        try:
            data_del_giorno = datetime(year, month, day)

            results = self.session.query(TOrdiniSchede).filter(
                TOrdiniSchede.data == data_del_giorno,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkOrdine': result.fkOrdine,
                'fkReparto': result.fkReparto,
                'data': result.data,
                'fkServizio': result.fkServizio,
                'cognome': result.cognome,
                'nome': result.nome,
                'letto': result.letto,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500
        
    def get_all_by_ordine(self,fkOrdine , servizio: int):
        """Recupera tutti i record da TOrdiniSchede per un giorno specifico e che non sono stati cancellati."""
        try:
            

            results = self.session.query(TOrdiniSchede).filter(
                TOrdiniSchede.fkOrdine == fkOrdine,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkOrdine': result.fkOrdine,
                'fkReparto': result.fkReparto,
                'data': result.data,
                'fkServizio': result.fkServizio,
                'cognome': result.cognome,
                'nome': result.nome,
                'letto': result.letto,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500    


    
    def get_count_filtrati(self, year: int, month: int, day: int, servizio: int, fkReparto=None, fkScheda=None):
        """Conta tutti i record da TOrdiniSchede per un giorno specifico e che non sono stati cancellati."""
        try:
            data_del_giorno = datetime(year, month, day)
            
            query = self.session.query(
                TOrdiniSchede.fkReparto,
                TOrdiniSchede.fkScheda,
                func.count().label('schede_count')
            ).filter(
                TOrdiniSchede.data == data_del_giorno,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            )

            if fkReparto is not None:
                query = query.filter(TOrdiniSchede.fkReparto == fkReparto)

            if fkScheda is not None:
                query = query.filter(TOrdiniSchede.fkScheda == fkScheda)

            results = query.group_by(TOrdiniSchede.fkReparto, TOrdiniSchede.fkScheda).all()

            # Organizza i risultati in un dizionario per facile accesso
            schede_count = {}
            for result in results:
                if result.fkReparto not in schede_count:
                    schede_count[result.fkReparto] = {}
                schede_count[result.fkReparto][result.fkScheda] = result.schede_count

            return schede_count
        except Exception as e:
            return {'Error': str(e)}, 500

        
    def get_by_id(self, id):
        try:
            result = self.session.query(TOrdiniSchede).filter_by(id=id).first()
        except Exception as e:
            return {'Error': str(e)}, 400
        if result:
            return {'id': result.id, 
                    'fkOrdine': result.fkOrdine,
                    'fkReparto': result.fkReparto, 
                    'data': result.data, 
                    'fkServizio': result.fkServizio,
                    'fkScheda' : result.fkScheda, 
                    'cognome': result.cognome,
                    'nome': result.nome, 
                    'letto': result.letto,
                    'dataInserimento': result.dataInserimento, 
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione, 
                    'utenteCancellazione': result.utenteCancellazione}
        else:
            return {'Error': f'No match found for this id: {id}'}, 404

    def create(self, fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto,  utenteInserimento):
        try:
            ordine = TOrdiniSchede(
                fkOrdine=fkOrdine,
                fkReparto=fkReparto, 
                data=data, 
                fkServizio=fkServizio, 
                fkScheda=fkScheda,
                cognome=cognome, 
                nome=nome, 
                letto=letto,  
                utenteInserimento=utenteInserimento
            )
            self.session.add(ordine)
            self.session.commit()
            return ordine.id
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def update(self, id, fkOrdine, fkReparto, data, fkServizio, fkScheda, cognome, nome, letto, utenteInserimento):
        try:
            ordine = self.session.query(TOrdiniSchede).filter_by(id=id).first()
            if ordine:
                ordine.fkOrdine = fkOrdine
                ordine.fkReparto = fkReparto
                ordine.data = data
                ordine.fkServizio = fkServizio
                ordine.fkScheda = fkScheda
                ordine.cognome = cognome
                ordine.nome = nome
                ordine.letto = letto
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
            ordine = self.session.query(TOrdiniSchede).filter_by(id=id).first()
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



