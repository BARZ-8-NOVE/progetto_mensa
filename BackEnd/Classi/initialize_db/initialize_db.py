
from Classi.ClasseDB.db_connection import engine, SessionLocal
from sqlalchemy.orm import sessionmaker

from Classi.ClasseUtility.UtilityCSV.CSV_Utils import populate_from_csv_with_ids

from Classi.ClasseServizi.Domani_t_servizi import TServizi
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi

from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Domain_t_ordiniPiatti import TOrdiniPiatti

from Classi.ClasseAlimenti.Classe_t_alimenti.Domani_t_alimenti import TAlimenti
from Classi.ClasseAlimenti.Classe_t_allergeni.Domani_t_allergeni import TAllergeni
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Domani_t_tipologiaalimenti import TTipologiaAlimenti
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Domani_t_tipologiaconservazione import TTipologiaConservazioni

from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Domain_t_tipoPreparazioni import TTipiPreparazioni
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Domain_t_preparazioni import TPreparazioni
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Domain_t_tipiquantita import TTipoQuantita
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Domani_t_preparazionicontenuti import TPreparazioniContenuti

from Classi.ClassePiatti.Classe_t_piatti.Domain_t_piatti import TPiatti
from Classi.ClassePiatti.Classe_t_tipiPiatti.Domani_t_tipiPiatti import TTipiPiatti
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione
from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu
from Classi.ClasseMenu.Classe_t_menu.Domain_t_menu import TMenu

from Classi.ClasseReparti.Domain_t_reparti import TReparti

def initialize_database():
    Session = sessionmaker(bind=engine)
    session = Session()

    session = SessionLocal()
    try:

        # Popolare la tabella
        populate_from_csv_with_ids(session, TReparti, 'DBMS/file_dati_statici/t_reparti.csv')
        populate_from_csv_with_ids(session, TServizi, 'DBMS/file_dati_statici/t_servizi.csv')
        populate_from_csv_with_ids(session, TAllergeni, 'DBMS/file_dati_statici/t_allergeni.csv')
        populate_from_csv_with_ids(session, TTipologiaConservazioni, 'DBMS/file_dati_statici/t_tipologiaconservazione.csv')        
        populate_from_csv_with_ids(session, TTipologiaAlimenti, 'DBMS/file_dati_statici/t_tipologiaalimenti.csv')        
        populate_from_csv_with_ids(session, TAlimenti, 'DBMS/file_dati_statici/t_tabella_alimenti_con_allergeni.csv')
        populate_from_csv_with_ids(session, TTipoQuantita, 'DBMS/file_dati_statici/t_tipoquantita.csv')
        populate_from_csv_with_ids(session, TTipiPreparazioni, 'DBMS/file_dati_statici/t_tipipreparazioni.csv')
        populate_from_csv_with_ids(session, TPreparazioni, 'DBMS/file_dati_statici/t_preparazioni.csv')
        populate_from_csv_with_ids(session, TPreparazioniContenuti, 'DBMS/file_dati_statici/t_preparazionicontenuti.csv')
        populate_from_csv_with_ids(session, TTipiPiatti, 'DBMS/file_dati_statici/t_tipiPiatti.csv')    
        populate_from_csv_with_ids(session, TPiatti, 'DBMS/file_dati_statici/t_piatti.csv')
        populate_from_csv_with_ids(session, TTipiMenu, 'DBMS/file_dati_statici/t_tipimenu.csv')
        populate_from_csv_with_ids(session, TMenu, 'DBMS/file_dati_statici/t_menu.csv')    
        populate_from_csv_with_ids(session, TMenuServizi, 'DBMS/file_dati_statici/t_menuservizi.csv')   
        populate_from_csv_with_ids(session, TAssociazionePiattiPreparazioni, 'DBMS/file_dati_statici/t_associazionepiattipreparazioni.csv')
        populate_from_csv_with_ids(session, TOrdini, 'DBMS/file_dati_statici/t_ordini.csv')
        populate_from_csv_with_ids(session, TOrdiniPiatti, 'DBMS/file_dati_statici/t_ordinipiatti.csv')

    except Exception as e:
                print(f"Errore durante il popolamento delle tabelle: {e}")
                session.rollback()
    finally:
                # Chiudere la sessione
            session.close()

def init_database():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        populate_from_csv_with_ids(session, TMenuServiziAssociazione, 'DBMS/file_dati_statici/output.csv')
    except Exception as e:
        print(f"Errore durante il popolamento delle tabelle: {e}")
        session.rollback()
    finally:
        session.close()

