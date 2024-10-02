from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordiniSchede.Domain_t_ordiniSchede import TOrdiniSchede
from Classi.ClasseSchede.Classe_t_schede.Domani_t_schede import TSchede
from Classi.ClasseMenu.Classe_t_menu.Repository_t_menu import TMenu
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
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()  # Ensure session is closed


    def get_by_day_and_nome_cognome(self, data, nome: str, cognome: str, servizio: int):
        """Recupera tutti i record da TOrdiniSchede per un giorno, nome e cognome specifici, e un servizio specifico, solo per dipendenti e che non sono stati cancellati."""
        try:
            result = self.session.query(TOrdiniSchede).join(TSchede, TOrdiniSchede.fkScheda == TSchede.id).filter(
                TOrdiniSchede.data == data,
                TOrdiniSchede.nome == nome,
                TOrdiniSchede.cognome == cognome,
                TOrdiniSchede.fkServizio == servizio,
                TSchede.dipendente == 1,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).first()

            if result:
                return {
                    'id': result.id,
                    'fkOrdine': result.fkOrdine,
                    'fkReparto': result.fkReparto,
                    'data': result.data,
                    'fkServizio': result.fkServizio,
                    'fkScheda': result.fkScheda,
                    'cognome': result.cognome,
                    'nome': result.nome,
                    'letto': result.letto,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                }
            else:
                return None

        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

        finally:
            self.session.close()  # Ensure session is closed
        


    def get_all_by_day_and_reparto(self, data, fkReparto: int, servizio: int, scheda: int):
        """Recupera tutti i record da TOrdiniSchede per un giorno e un reparto specifico e che non sono stati cancellati."""
        try:


            results = self.session.query(TOrdiniSchede).filter(
                TOrdiniSchede.data == data,
                TOrdiniSchede.fkReparto == fkReparto,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.fkScheda == scheda,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkOrdine': result.fkOrdine,
                'fkReparto': result.fkReparto,
                'data': result.data,
                'fkServizio': result.fkServizio,
                'fkScheda': result.fkScheda,
                'cognome': result.cognome,
                'nome': result.nome,
                'letto': result.letto,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_all_by_ordine(self,fkOrdine):
        """Recupera tutti i record da TOrdiniSchede per un giorno specifico e che non sono stati cancellati."""
        try:
            

            results = self.session.query(TOrdiniSchede).filter(
                TOrdiniSchede.fkOrdine == fkOrdine,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkOrdine': result.fkOrdine,
                'fkReparto': result.fkReparto,
                'data': result.data,
                'fkServizio': result.fkServizio,
                'fkScheda': result.fkScheda,
                'cognome': result.cognome,
                'nome': result.nome,
                'letto': result.letto,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500    
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_all_by_ordine_per_stampa(self, fkOrdine):
        """Recupera i record da TOrdiniSchede per un giorno specifico, raggruppando i brodi per reparto e lasciando gli altri non raggruppati."""
        try:
            # Recupera tutte le schede per l'ordine specificato che non sono cancellate
            results = self.session.query(TOrdiniSchede).filter(
                TOrdiniSchede.fkOrdine == fkOrdine,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).order_by(TOrdiniSchede.fkReparto, TOrdiniSchede.letto).all()

            # Dizionario per raggruppare i brodi per reparto (schede con fkScheda == 18)
            schede_per_reparto = {}
            response = []

            for result in results:
                # Se la scheda è diversa da 18, la aggiungiamo direttamente al risultato
                if result.fkScheda != 18:
                    response.append({
                        'id': result.id,
                        'fkOrdine': result.fkOrdine,
                        'fkReparto': result.fkReparto,
                        'data': result.data,
                        'fkServizio': result.fkServizio,
                        'fkScheda': result.fkScheda,
                        'cognome': result.cognome,
                        'nome': result.nome,
                        'letto': result.letto,
                        'dataInserimento': result.dataInserimento,
                        'utenteInserimento': result.utenteInserimento,
                        'dataCancellazione': result.dataCancellazione,
                        'utenteCancellazione': result.utenteCancellazione
                    })
                else:
                    # Raggruppiamo i brodi (schede con fkScheda == 18) per reparto
                    fkReparto = result.fkReparto
                    if fkReparto not in schede_per_reparto:
                        schede_per_reparto[fkReparto] = {
                            'count': 0,
                            'first_scheda': None
                        }

                    # Incrementiamo il conteggio delle schede per il reparto
                    schede_per_reparto[fkReparto]['count'] += 1

                    # Se questa è la prima scheda del reparto, la salviamo
                    if schede_per_reparto[fkReparto]['first_scheda'] is None:
                        schede_per_reparto[fkReparto]['first_scheda'] = {
                            'id': result.id,
                            'fkOrdine': result.fkOrdine,
                            'fkReparto': result.fkReparto,
                            'data': result.data,
                            'fkServizio': result.fkServizio,
                            'fkScheda': result.fkScheda,
                            'cognome': result.cognome,
                            'nome': result.nome,
                            'letto': result.letto,
                            'dataInserimento': result.dataInserimento,
                            'utenteInserimento': result.utenteInserimento,
                            'dataCancellazione': result.dataCancellazione,
                            'utenteCancellazione': result.utenteCancellazione
                        }

            # Aggiungiamo le schede dei brodi (fkScheda == 18) con il conteggio per reparto
            for fkReparto, info in schede_per_reparto.items():
                first_scheda = info['first_scheda']
                first_scheda['numeroSchede'] = info['count']  # Aggiungiamo il numero di schede per reparto
                response.append(first_scheda)

            return response

        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()





    def count_brodi(self, data, fkOrdine: int, fkScheda=18):
        """Conta tutti i record da TOrdiniSchede per un giorno specifico e che non sono stati cancellati."""
        try:
            # Costruzione della query
            query = self.session.query(
                TOrdiniSchede.fkReparto,
                TOrdiniSchede.fkScheda,
                func.count().label('schede_count')
            ).filter(
                TOrdiniSchede.data == data,
                TOrdiniSchede.fkOrdine == fkOrdine,
                TOrdiniSchede.dataCancellazione.is_(None),
                TOrdiniSchede.fkScheda == fkScheda,  # Utilizza il parametro fkScheda
            ).group_by(
                TOrdiniSchede.fkReparto,
                TOrdiniSchede.fkScheda
            )

            # Esecuzione della query
            results = query.all()

            # Organizzazione dei risultati in un dizionario
            schede_count = {}
            for result in results:
                if result.fkReparto not in schede_count:
                    schede_count[result.fkReparto] = {}
                schede_count[result.fkReparto][result.fkScheda] = result.schede_count

            return schede_count
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()





    
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
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()





    def count_totali_tipo_menu(self, anno: int, mese=None, giorno=None):
        """Conta il totale degli ordini per un mese specifico e restituisce il totale per tipo di menu, 
        inclusi i brodi (fkScheda=18) come una categoria separata."""
        try:
            # Conteggio generale degli ordini raggruppati per tipo di menu (escludendo fkScheda=18)
            conteggi_menu = (
                self.session.query(
                    TSchede.fkTipoMenu,
                    func.count(TOrdiniSchede.id).label('conteggio')
                )
                .join(TOrdiniSchede, TOrdiniSchede.fkScheda == TSchede.id)
                .filter(
                    TOrdiniSchede.dataCancellazione.is_(None),
                    TOrdiniSchede.fkScheda != 18,
                    (func.extract('year', TOrdiniSchede.data) == anno) | (anno is None),
                    (func.extract('month', TOrdiniSchede.data) == mese) | (mese is None),
                    (func.extract('day', TOrdiniSchede.data) == giorno) | (giorno is None)
                )
                .group_by(TSchede.fkTipoMenu)
                
                .all()
            )

            # Conteggio separato per la scheda fkScheda=18 (brodi)
            conteggio_brodi = (
                self.session.query(func.count(TOrdiniSchede.id))
                .filter(
                    TOrdiniSchede.fkScheda == 18,
                    TOrdiniSchede.dataCancellazione.is_(None),
                    (func.extract('year', TOrdiniSchede.data) == anno) | (anno is None),
                    (func.extract('month', TOrdiniSchede.data) == mese) | (mese is None),
                    (func.extract('day', TOrdiniSchede.data) == giorno) | (giorno is None)
                )
                .scalar()
            )

            # Creazione di un dizionario per i risultati
            risultati = {menu.fkTipoMenu: menu.conteggio for menu in conteggi_menu}

            # Aggiungi il conteggio della scheda 18 come 'brodi'
            risultati['brodi'] = conteggio_brodi

            return {
                'conteggi_menu': risultati
            }
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()



    def count_totali_per_giorno(self, data, servizio: int):
        """Conta il totale degli ordini per pazienti e personale in una data specifica, e restituisce i totali complessivi."""
        try:
            # Query per il totale degli ordini per pazienti
            totale_pazienti = self.session.query(func.count()).select_from(
                TOrdiniSchede
            ).join(
                TSchede, TOrdiniSchede.fkScheda == TSchede.id
            ).filter(
                TSchede.dipendente == 0,
                TOrdiniSchede.data == data,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).scalar()  # Usa scalar() per ottenere il valore del conteggio direttamente

            # Query per il totale degli ordini per personale
            totale_personale = self.session.query(func.count()).select_from(
                TOrdiniSchede
            ).join(
                TSchede, TOrdiniSchede.fkScheda == TSchede.id
            ).filter(
                TSchede.dipendente == 1,
                TOrdiniSchede.data == data,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).scalar()  # Usa scalar() per ottenere il valore del conteggio direttamente

            # Calcolo del totale complessivo
            totale_completo = totale_pazienti + totale_personale

            return {
                'totale_pazienti': totale_pazienti,
                'totale_personale': totale_personale,
                'totale_completo': totale_completo
            }
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()





    def count_totali_per_mese(self, mese: int, anno: int, servizio: int):
        """Conta il totale degli ordini per un mese specifico e restituisce il totale complessivo per servizio."""
        try:
            # Query per il totale degli ordini (senza distinzione tra pazienti e personale)
            totale_completo = self.session.query(func.count()).select_from(
                TOrdiniSchede
            ).join(
                TSchede, TOrdiniSchede.fkScheda == TSchede.id
            ).filter(
                func.extract('month', TOrdiniSchede.data) == mese,
                func.extract('year', TOrdiniSchede.data) == anno,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).scalar()  # Usa scalar() per ottenere il valore del conteggio direttamente

            return {
                'totale_completo': totale_completo
            }
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()


    def count_totali_per_anno(self, anno: int, servizio: int):
        """Conta il totale degli ordini per un anno specifico e restituisce il totale complessivo per servizio."""
        try:
            # Query per il totale degli ordini (senza distinzione tra pazienti e personale)
            totale_completo = self.session.query(func.count()).select_from(
                TOrdiniSchede
            ).join(
                TSchede, TOrdiniSchede.fkScheda == TSchede.id
            ).filter(
                func.extract('year', TOrdiniSchede.data) == anno,
                TOrdiniSchede.fkServizio == servizio,
                TOrdiniSchede.dataCancellazione.is_(None)
            ).scalar()  # Usa scalar() per ottenere il valore del conteggio direttamente

            return {
                'totale_completo': totale_completo
            }
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()

        
    def get_by_id(self, id):
        try:
            # Esegui la query per recuperare il record con l'id specificato
            result = self.session.query(TOrdiniSchede).filter_by(id=id).first()
            
            if result:
                # Restituisci i dati del record come dizionario
                return {'id': result.id, 
                        'fkOrdine': result.fkOrdine,
                        'fkReparto': result.fkReparto, 
                        'data': result.data, 
                        'fkServizio': result.fkServizio,
                        'fkScheda': result.fkScheda, 
                        'cognome': result.cognome,
                        'nome': result.nome, 
                        'letto': result.letto,
                        'dataInserimento': result.dataInserimento, 
                        'utenteInserimento': result.utenteInserimento,
                        'dataCancellazione': result.dataCancellazione, 
                        'utenteCancellazione': result.utenteCancellazione}
            else:
                # Restituisci un errore se non viene trovato alcun record
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            # Gestisci eventuali errori restituendo un messaggio di errore e un codice di stato 400
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def check_letto(self, fkOrdine, fkReparto, data, fkServizio, letto):
        try:
            # Esegui la query per recuperare il record con i criteri specificati
            result = self.session.query(TOrdiniSchede).filter_by(
                fkOrdine=fkOrdine,
                fkReparto=fkReparto,
                data=data,
                fkServizio=fkServizio,
                letto=letto,
                dataCancellazione=None  # Verifica che il record non sia stato cancellato
            ).first()

            # Se esiste un record e appartiene a un altro ordine, restituisci il numero del letto
            if result:
                return result.letto  # Restituisce il numero del letto occupato
            return False  # Letto disponibile

        except Exception as e:
            self.session.rollback()
            # Log l'errore per tracciabilità
            print(f"Error in check_letto: {str(e)}")  # Puoi sostituirlo con un logger
            return {'Error': str(e)}, 400

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()




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
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

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
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

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
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()



