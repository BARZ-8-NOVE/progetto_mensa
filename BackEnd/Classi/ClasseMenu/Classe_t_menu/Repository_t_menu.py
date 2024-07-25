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

from datetime import datetime 
from sqlalchemy import and_
class RepositoryMenu:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

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
            logging.error(f"Error getting all menu: {e}")
            return {'Error': str(e)}, 500
        

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
            logging.error(f"Error getting menu by month: {e}")
            return {'Error': str(e)}, 500




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
            logging.error(f"Error getting menu by ID {id}: {e}")
            return {'Error': str(e)}, 400

    def create(self, data, fkTipoMenu,  utenteInserimento):
        try:
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
            logging.error(f"Error fetching menu details: {e}")
            return {'Error': str(e)}, 500

    def _get_end_date_of_month(self, year: int, month: int):
        if month == 12:
            return datetime(year + 1, 1, 1)  # Primo giorno dell'anno successivo
        else:
            return datetime(year, month + 1, 1)  # Primo giorno del mese successivo
        



   