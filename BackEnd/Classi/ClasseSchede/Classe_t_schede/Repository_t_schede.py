from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schede.Domani_t_schede import TSchede
from datetime import datetime

class RepositoryTSchede:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()





    def get_by_id(self, id):
            try:
                result = self.session.query(TSchede).filter_by(id=id).first()
                if result:
                    return {'id': result.id, 
                        'fkTipoAlimentazione': result.fkTipoAlimentazione, 
                        'fkTipoMenu': result.fkTipoMenu,
                        'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                        'nome': result.nome, 
                        'titolo': result.titolo, 
                        'sottotitolo': result.sottotitolo, 
                        'descrizione': result.descrizione, 
                        'backgroundColor': result.backgroundColor, 
                        'color': result.color, 
                        'dipendente': result.dipendente, 
                        'note': result.note,
                        'inizio': result.inizio,
                        'fine': result.fine,
                        'ordinatore': result.ordinatore,
                        'dataInserimento': result.dataInserimento, 
                        'utenteInserimento': result.utenteInserimento, 
                        'dataCancellazione': result.dataCancellazione, 
                        'utenteCancellazione': result.utenteCancellazione, 
                        'nominativa': result.nominativa 
                 
                        }
                else:
                    return {'Error': f'No match found for this id: {id}'}, 404
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 400
            
            finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()


    def get_all(self):
        try:
            # Esegui la query per ottenere tutti i risultati non cancellati
            results = self.session.query(TSchede).filter(TSchede.dataCancellazione.is_(None)).all()
            
            # Costruisci la lista dei risultati
            output = [{'id': result.id, 
                'fkTipoAlimentazione': result.fkTipoAlimentazione, 
                'fkTipoMenu': result.fkTipoMenu,
                'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                'nome': result.nome, 
                'titolo': result.titolo, 
                'sottotitolo': result.sottotitolo, 
                'descrizione': result.descrizione, 
                'backgroundColor': result.backgroundColor, 
                'color': result.color, 
                'dipendente': result.dipendente, 
                'note': result.note,
                'inizio': result.inizio,
                'fine': result.fine,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione, 
                'nominativa': result.nominativa 
                    } for result in results]
            return output
        
        except Exception as e:
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error fetching data: {str(e)}")
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_all_attivi_pazienti(self):
        try:
            # Esegui la query per ottenere tutte le schede attive per i pazienti (dipendente == 0)
            results = self.session.query(TSchede).filter(
                TSchede.utenteCancellazione.is_(None),  # Verifica se utenteCancellazione è NULL
                TSchede.fine.is_(None),  # Verifica se fine è NULL
                TSchede.dipendente == 0  # Verifica se dipendente è 0
            ).order_by(TSchede.ordinatore).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'fkTipoAlimentazione': result.fkTipoAlimentazione, 
                'fkTipoMenu': result.fkTipoMenu,
                'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                'nome': result.nome, 
                'titolo': result.titolo, 
                'sottotitolo': result.sottotitolo, 
                'descrizione': result.descrizione, 
                'backgroundColor': result.backgroundColor, 
                'color': result.color, 
                'dipendente': result.dipendente, 
                'note': result.note,
                'inizio': result.inizio,
                'fine': result.fine,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione, 
                'nominativa': result.nominativa 
            } for result in results]
        
        except Exception as e:
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error fetching data: {str(e)}")
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()




    def get_all_personale(self):
        try:
            # Esegui la query per ottenere tutte le schede attive per i dipendenti (dipendente == 1)
            results = self.session.query(TSchede).filter(
                TSchede.utenteCancellazione.is_(None),  # Verifica se utenteCancellazione è NULL
                TSchede.fine.is_(None),  # Verifica se fine è NULL
                TSchede.dipendente == 1  # Verifica se dipendente è 1
            ).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'fkTipoAlimentazione': result.fkTipoAlimentazione, 
                'fkTipoMenu': result.fkTipoMenu,
                'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                'nome': result.nome, 
                'titolo': result.titolo, 
                'sottotitolo': result.sottotitolo, 
                'descrizione': result.descrizione, 
                'backgroundColor': result.backgroundColor, 
                'color': result.color, 
                'dipendente': result.dipendente, 
                'note': result.note,
                'inizio': result.inizio,
                'fine': result.fine,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione, 
                'nominativa': result.nominativa 
            } for result in results]
        
        except Exception as e:
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error fetching data: {str(e)}")
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def create(self, fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa):
        try:
            # Verifica i valori che stai cercando di inserire
            print(f"Inserimento dati: fkTipoAlimentazione={fkTipoAlimentazione}, fkTipoMenu={fkTipoMenu}, nome={nome}, titolo={titolo}, sottotitolo={sottotitolo}, descrizione={descrizione}, backgroundColor={backgroundColor}, dipendente={dipendente}, note={note}, inizio={inizio}, fine={fine}, utenteInserimento={utenteInserimento}, nominativa={nominativa}")

            # Crea l'oggetto TSchede
            scheda = TSchede(
                fkTipoAlimentazione=fkTipoAlimentazione,
                fkTipoMenu=fkTipoMenu,
                nome=nome,
                titolo=titolo,
                sottotitolo=sottotitolo,
                descrizione=descrizione,
                backgroundColor=backgroundColor,
                dipendente=1 if dipendente else 0,  # Converti True/False a 1/0 per SmallInteger
                note=note,
                inizio=inizio,
                fine=fine,
                utenteInserimento=utenteInserimento,
                nominativa=1 if nominativa else 0  # Converti True/False a 1/0 per SmallInteger
            )

            # Aggiungi l'oggetto alla sessione
            self.session.add(scheda)

            # Esegui il commit
            self.session.commit()

            print("Scheda aggiunta con successo!")
            return {'Message': 'Scheda added successfully!'}, 200

        except Exception as e:
            # Rollback in caso di errore
            self.session.rollback()

            # Stampa l'errore per il debug
            print(f"Error during database commit: {str(e)}")

            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def update(self, id, fkTipoAlimentazione, fkTipoMenu, nome, titolo, sottotitolo, descrizione, backgroundColor, dipendente, note, inizio, fine, utenteInserimento, nominativa):
        try:
            scheda = self.session.query(TSchede).filter_by(id=id).first()
            if scheda:
                scheda.id = id
                scheda.fkTipoAlimentazione = fkTipoAlimentazione
                scheda.fkTipoMenu = fkTipoMenu
                scheda.nome = nome
                scheda.titolo = titolo
                scheda.sottotitolo = sottotitolo
                scheda.descrizione = descrizione
                scheda.backgroundColor = backgroundColor
                scheda.dipendente = 1 if dipendente else 0  # Converti True/False a 1/0 per SmallInteger
                scheda.note = note
                scheda.inizio = inizio
                scheda.fine = fine
                scheda.utenteInserimento = utenteInserimento
                scheda.nominativa = 1 if nominativa else 0
                
                self.session.commit()
                return {'Message': 'Scheda updated successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            scheda = self.session.query(TSchede).filter_by(id=id).first()
            if scheda:
                scheda.dataCancellazione = datetime.now()
                scheda.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'Message': 'Scheda deleted successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()