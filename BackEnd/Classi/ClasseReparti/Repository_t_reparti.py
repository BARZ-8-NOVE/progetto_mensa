from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseReparti.Domain_t_reparti import TReparti
from datetime import datetime

class RepositoryReparti:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TReparti).filter(TReparti.dataCancellazione.is_(None)).all()
            return [{'id': result.id, 'codiceAreas': result.codiceAreas, 'descrizione': result.descrizione,
                     'sezione': result.sezione, 'ordinatore': result.ordinatore, 'padiglione': result.padiglione,
                     'piano': result.piano, 'lato': result.lato, 'inizio': result.inizio, 'fine': result.fine,
                     'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento,
                     'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
                    for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TReparti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'codiceAreas': result.codiceAreas, 'descrizione': result.descrizione,
                        'sezione': result.sezione, 'ordinatore': result.ordinatore, 'padiglione': result.padiglione,
                        'piano': result.piano, 'lato': result.lato, 'inizio': result.inizio, 'fine': result.fine,
                        'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento,
                        'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400

    def get_by_ids(self, ids):
        try:
            # Assicurati che 'ids' sia una lista di numeri interi
            if not isinstance(ids, list) or not all(isinstance(id, int) for id in ids):
                return {'Error': 'IDs should be provided as a list of integers'}, 400
            
            # Filtra i risultati per ID
            results = self.session.query(TReparti).filter(TReparti.id.in_(ids)).all()
            
            # Se non ci sono risultati, ritorna un errore
            if not results:
                return {'Error': f'No matches found for these IDs: {ids}'}, 404
            
            # Mappa i risultati in un dizionario
            result_list = []
            for result in results:
                result_list.append({
                    'id': result.id,
                    'codiceAreas': result.codiceAreas,
                    'descrizione': result.descrizione,
                    'sezione': result.sezione,
                    'ordinatore': result.ordinatore,
                    'padiglione': result.padiglione,
                    'piano': result.piano,
                    'lato': result.lato,
                    'inizio': result.inizio,
                    'fine': result.fine,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                })
            
            return {'results': result_list}
            
        except Exception as e:
            return {'Error': str(e)}, 400




    def create(self, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento):
        try:
            reparto = TReparti(
                codiceAreas=codiceAreas, 
                descrizione=descrizione, 
                sezione=sezione, 
                ordinatore=ordinatore,
                padiglione=padiglione, 
                piano=piano, 
                lato=lato, 
                inizio=inizio, 
                fine=fine,
                dataInserimento=dataInserimento, 
                utenteInserimento=utenteInserimento
            )
            self.session.add(reparto)
            self.session.commit()
            return {'Message': 'Reparto added successfully!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def update(self, id, codiceAreas, descrizione, sezione, ordinatore, padiglione, piano, lato, inizio, fine, dataInserimento, utenteInserimento):
        try:
            reparto = self.session.query(TReparti).filter_by(id=id).first()
            if reparto:
                reparto.codiceAreas = codiceAreas
                reparto.descrizione = descrizione
                reparto.sezione = sezione
                reparto.ordinatore = ordinatore
                reparto.padiglione = padiglione
                reparto.piano = piano
                reparto.lato = lato
                reparto.inizio = inizio
                reparto.fine = fine
                reparto.dataInserimento = dataInserimento
                reparto.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'Message': 'Reparto updated successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete(self, id, utenteCancellazione):
        try:
            reparto = self.session.query(TReparti).filter_by(id=id).first()
            if reparto:
                reparto.dataCancellazione = datetime.now()
                reparto.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'Message': 'Reparto deleted successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
