import logging
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseMenu.Classe_t_menu.Domain_t_menu import TMenu
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from Classi.ClassePiatti.Classe_t_piatti.Domain_t_piatti import TPiatti
from Classi.ClasseServizi.Domani_t_servizi import TServizi
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Domain_t_preparazioni import TPreparazioni
from sqlalchemy.exc import SQLAlchemyError


        
from datetime import datetime, date, timedelta
from sqlalchemy import and_, func
class RepositoryMenu:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def get_all(self):
        try:
            results = self.session.query(TMenu).filter(TMenu.dataCancellazione.is_(None)).all()
            return [
                {
                    'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting all menu: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_by_mese_corrente(self, year: int, month: int, fkTipoMenu: int = None):
        try:
            # Calcola la data di inizio e fine del mese
            start_date = datetime(year, month, 1)
            end_date = self._get_end_date_of_month(year, month)

            # Costruisci la query con eventuale filtro per tipo di menu
            query = self.session.query(TMenu).filter(
                and_(
                    TMenu.data >= start_date,
                    TMenu.data < end_date,
                    TMenu.dataCancellazione.is_(None)
                )
            )

            # Aggiungi il filtro per fkTipoMenu se fornito
            if fkTipoMenu is not None:
                query = query.filter(TMenu.fkTipoMenu == fkTipoMenu)

            results = query.all()

            return [
                {
                    'id': result.id,
                    'data': result.data.strftime('%Y-%m-%d'),  # Converti la data in formato stringa
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting menu by month: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()  

    def get_by_date_range(self, start_date: datetime, end_date: datetime, fkTipoMenu: int = None):
        try:
            # Assicurati che le date di fine siano incluse
            end_date = end_date + timedelta(days=1)

            # Costruisci la query con eventuale filtro per tipo di menu
            query = self.session.query(TMenu).filter(
                and_(
                    TMenu.data >= start_date,
                    TMenu.data < end_date,
                    TMenu.dataCancellazione.is_(None)
                )
            )

            # Aggiungi il filtro per fkTipoMenu se fornito
            if fkTipoMenu is not None:
                query = query.filter(TMenu.fkTipoMenu == fkTipoMenu)

            results = query.all()

            return [
                {
                    'id': result.id,
                    'data': result.data.strftime('%Y-%m-%d'),  # Converti la data in formato stringa
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
            
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting menu by date range: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_by_id(self, id):
        try:
            result = self.session.query(TMenu).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                }
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting menu by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()  

    def create(self, data, fkTipoMenu, utenteInserimento):
        try:
            # Controlla se un elemento con data e fkTipoMenu esiste già
            existing_menu = self.session.query(TMenu).filter_by(data=data, fkTipoMenu=fkTipoMenu).first()
            
            if existing_menu:
                # Se esiste, restituisce un messaggio di errore
                return {'Error': 'Elemento già esistente'}, 400
            
            # Se non esiste, crea un nuovo elemento
            menu = TMenu(
                data=data,
                fkTipoMenu=fkTipoMenu,
                utenteInserimento=utenteInserimento
            )
            self.session.add(menu)
            self.session.commit()
            return menu.id
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating menu: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()  

    def update(self, id, data, fkTipoMenu, dataInserimento, utenteInserimento):
        try:
            menu = self.session.query(TMenu).filter_by(id=id).first()
            if menu:
                menu.data = data
                menu.fkTipoMenu = fkTipoMenu
                menu.dataInserimento = dataInserimento
                menu.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'menu': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating menu with ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()  
            
    def get_by_date_and_type(self, year, month, day, fkTipoMenu):
        target_date = date(year, month, day)
        try:
            # Esegui la query per recuperare il record basato su data e fkTipoMenu
            result = self.session.query(TMenu).filter_by(data=target_date, fkTipoMenu=fkTipoMenu).first()
            return result
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            # Gestisci eventuali errori e restituisci un messaggio di errore
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_by_data(self, data, fkTipoMenu):
        try:
            # Effettua la query per ottenere il menu per la data e tipo di menu specificati
            result = self.session.query(TMenu).filter_by(
                data=data,
                fkTipoMenu=fkTipoMenu
            ).filter(TMenu.dataCancellazione.is_(None)).first()
            
            if result:
                # Restituisce i dettagli del menu come dizionario
                return {
                    'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                }
            else:
                 # Restituisce None se non ci sono risultati
                return None

        except SQLAlchemyError as e:
            self.session.rollback()  # Aggiunta del rollback
            # Gestione degli errori specifici di SQLAlchemy
            logging.error(f"SQLAlchemy error getting menu by date {data}: {e}")
            raise RuntimeError("Database error occurred") from e

        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            # Gestione di altri errori generali
            logging.error(f"Unexpected error getting menu by date {data}: {e}")
            raise RuntimeError(f"Unexpected error: {str(e)}") from e

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    
    def delete(self, id, utenteCancellazione):
        try:
            menu = self.session.query(TMenu).filter_by(id=id).first()
            if menu:
                menu.dataCancellazione = datetime.now()
                menu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'menu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting menu by ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()  



    def get_menu_details(self, year: int, month: int, tipo_menu: int, id_menu: int):
        try:
            start_date = datetime(year, month, 1)
            end_date = self._get_end_date_of_month(year, month)

            # Esegui la query
            results = self.session.query(
                TPiatti.titolo.label('piatto_titolo'),
                TPreparazioni.descrizione.label('preparazione_descrizione'),
                TServizi.descrizione.label('servizio_descrizione')
            ).join(
                TMenuServizi, TMenuServizi.fkMenu == TMenu.id
            ).join(
                TMenuServiziAssociazione, TMenuServizi.id == TMenuServiziAssociazione.fkMenuServizio
            ).join(
                TAssociazionePiattiPreparazioni, TMenuServiziAssociazione.associazioni == TAssociazionePiattiPreparazioni.id
            ).join(
                TPiatti, TAssociazionePiattiPreparazioni.fkPiatto == TPiatti.id
            ).join(
                TPreparazioni, TAssociazionePiattiPreparazioni.fkPreparazione == TPreparazioni.id
            ).join(
                TServizi, TMenuServizi.fkServizio == TServizi.id
            ).join(
                TMenu, TMenu.id == TMenuServizi.fkMenu
            ).filter(
                and_(
                    TMenu.data >= start_date,
                    TMenu.data < end_date,
                    TMenu.dataCancellazione.is_(None),
                    TMenu.fkTipoMenu == tipo_menu,
                    TMenuServizi.dataCancellazione.is_(None),
                    TMenuServiziAssociazione.dataCancellazione.is_(None),
                    TMenuServizi == id_menu, 
                    TAssociazionePiattiPreparazioni.dataCancellazione.is_(None),
                    TPiatti.dataCancellazione.is_(None),
                    TPreparazioni.dataCancellazione.is_(None)
                )
            ).all()

            # Converti i risultati in una lista di dizionari
            return [
                {
                    'piatto_titolo': result.piatto_titolo,
                    'preparazione_descrizione': result.preparazione_descrizione,
                    'servizio_descrizione': result.servizio_descrizione,
                } for result in results
            ]

        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error fetching menu details: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close() 

    def _get_end_date_of_month(self, year: int, month: int):
        if month == 12:
            return datetime(year + 1, 1, 1)  # Primo giorno dell'anno successivo
        else:
            return datetime(year, month + 1, 1)  # Primo giorno del mese successivo
       



    def get_latest_by_fkTipoMenu(self):
        try:
            # Subquery per ottenere la data massima per ogni fkTipoMenu con dataCancellazione NULL
            subquery = self.session.query(
                TMenu.fkTipoMenu,
                func.max(TMenu.data).label('max_data')
            ).group_by(TMenu.fkTipoMenu).filter(TMenu.dataCancellazione.is_(None)).subquery()

            # Query principale per ottenere i dettagli del record più recente per ogni fkTipoMenu,
            # assicurandosi che anche la dataCancellazione sia NULL
            results = self.session.query(
                TMenu.id,
                TMenu.data,
                TMenu.fkTipoMenu,
                TMenu.dataInserimento,
                TMenu.utenteInserimento,
                TMenu.dataCancellazione,
                TMenu.utenteCancellazione
            ).join(
                subquery,
                (TMenu.fkTipoMenu == subquery.c.fkTipoMenu) & (TMenu.data == subquery.c.max_data)
            ).filter(TMenu.dataCancellazione.is_(None)).all()

            # Restituzione dei risultati come lista di dizionari
            return [{'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione} for result in results]

        except Exception as e:
            self.session.rollback()  # Esegui il rollback in caso di errore
            return {'Error': str(e)}, 500

        finally:
            self.session.close()  # Assicurati che la sessione venga chiusa
