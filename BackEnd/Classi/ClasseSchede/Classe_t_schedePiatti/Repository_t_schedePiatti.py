from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schedePiatti.Domain_t_schedePiatti import TSchedePiatti
from datetime import datetime

class RepositoryTSchedePiatti:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_piatti_by_scheda(self, fkScheda):
        results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
        
        return [{'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'note': result.note,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione
                } for result in results]
    
    def get_piatti_non_dolci_by_scheda(self, fkScheda, fkServizio):
        results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.colonna != 2,
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
        return [{'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'note': result.note,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione

                 
                } for result in results]
    

    def get_dolci_pane_by_scheda(self, fkScheda, fkServizio):
        results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.colonna == 2,
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
        return [{'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'note': result.note,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione

                 
                } for result in results]


    def get_piatti_by_scheda_and_servizio(self, fkScheda, fkServizio):
        results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
        return [{'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'note': result.note,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione

                 
                } for result in results]



    def create(self, fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, dataInserimento):
        try:
            scheda = TSchedePiatti(
                fkScheda=fkScheda,
                fkServizio=fkServizio,
                fkPiatto=fkPiatto, 
                colonna=colonna,
                riga=riga,
                note=note,
                ordinatore=ordinatore,
                dataInserimento=dataInserimento, 

            )
            self.session.add(scheda)
            self.session.commit()
            return 
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        

    def delete_piatti_Scheda(self, fkScheda, utenteCancellazione):
        try:
            # Ottieni tutte le associazioni corrispondenti a fkMenuServizio
            piattiScheda = self.session.query(TSchedePiatti).filter_by(fkScheda=fkScheda).all()
            
            # Se non ci sono associazioni, restituisci un errore
            if not piattiScheda:
                return {'Error': f'No match found for fkMenuServizio: {fkScheda}'}, 404
            
            # Esegui la soft delete per ciascuna associazione
            for associazione in piattiScheda:
                associazione.dataCancellazione = datetime.now()
                associazione.utenteCancellazione = utenteCancellazione
            
            # Commit le modifiche
            self.session.commit()
            return {'associazione': 'soft deleted!'}, 200
            
        except Exception as e:
            # Esegui il rollback in caso di errore
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

