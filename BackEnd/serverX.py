# Importare i controller
from datetime import datetime, date, timedelta, time, timezone

import calendar
import locale
from functools import wraps
import pprint
import logging
import traceback
from dateutil.relativedelta import relativedelta
from itsdangerous import URLSafeTimedSerializer

from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti
from Classi.ClasseUtenti.Classe_t_log.Service_t_log import Service_t_Log
 

from Classi.ClasseAlimenti.Classe_t_alimenti.Service_t_alimenti import Service_t_Alimenti
from Classi.ClasseAlimenti.Classe_t_allergeni.Service_t_allergeni import Service_t_Allergeni
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Service_t_tipologiaalimenti import Service_t_tipologiaalimenti

from Classi.ClasseMenu.Classe_t_tipiMenu.Service_t_tipiMenu import Service_t_TipiMenu
from Classi.ClasseMenu.Classe_t_menu.Service_t_menu import Service_t_Menu
from Classi.ClasseMenu.Classe_t_menuServizi.Service_t_menuServizi import Service_t_MenuServizi
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Service_t_menuServiziAssociazione import Service_t_MenuServiziAssociazione


from Classi.ClassePiatti.Classe_t_tipiPiatti.Service_t_tipiPiatti import Service_t_TipiPiatti
from Classi.ClassePiatti.Classe_t_piatti.Service_t_piatti import Service_t_Piatti
 
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Service_t_associazionePiattiPreparazioni import Service_t_AssociazionePiattiPreparazionie
from Classi.ClassePiatti.Classe_t_associazioneTipiPiattiTipiPreparazioni.Service_t_associazioneTipiPiattiTipiPreparazioni import Service_t_AssociazioneTipiPiattiTipiPreparazioni
from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Service_t_tipoPreparazioni import Service_t_tipipreparazioni
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Service_t_Preparazioni import Service_t_preparazioni
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Service_t_tipiquantita import Service_t_tipoquantita
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Service_t_preparazioniContenuti import Service_t_preparazionicontenuti

from Classi.ClasseDiete.Classe_t_tipiAlimentazione.Service_t_tipiAlimentazione import Service_t_TipiAlimentazione

from Classi.ClasseServizi.Service_t_servizi import Service_t_Servizi
from Classi.ClasseReparti.Service_t_reparti import Service_t_Reparti

from Classi.ClasseSchede.Classe_t_schede.Service_t_schede import Service_t_Schede
from Classi.ClasseSchede.Classe_t_schedePiatti.Service_t_schedePiatti import Service_t_SchedePiatti
from Classi.ClasseOrdini.Classe_t_ordini.Service_t_ordini import Service_t_Ordini
from Classi.ClasseOrdini.Classe_t_ordiniSchede.Service_t_ordiniSchede import Service_t_OrdiniSchede
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Service_t_ordiniPiatti import Service_t_OrdiniPiatti
from Classi.ClasseUtility import *

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, Blueprint, request, session, render_template, redirect, url_for, flash, abort
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies,  verify_jwt_in_request
from werkzeug.exceptions import NotFound, Forbidden
from datetime import timedelta
from werkzeug.utils import secure_filename
import os
import json

# Import your service modules here

from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseDB.config import DATABASE_URI, SECRET_KEY
from Classi.ClasseDB.config import EmailConfig
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseForm.form import (AlimentiForm, PreparazioniForm, AlimentoForm, PiattiForm, MenuForm, 
                                    LoginFormNoCSRF, schedaForm, ordineSchedaForm, schedaPiattiForm, 
                                    UtenteForm, CloneMenuForm, TipoUtenteForm , TipologiaPiattiForm, 
                                    TipologiaMenuForm, RepartiForm, ServiziForm, LogoutFormNoCSRF, 
                                    CambioPasswordForm, ordinedipendenteForm, ContattiForm, 
                                    PasswordResetRequestForm, ordineSchedaDipendentiForm,
                                    PasswordResetForm, CambioEmailForm)

# Initialize the app and configuration
import Reletionships



app = Flask(__name__)

# Carica configurazioni del DB
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['WTF_CSRF_ENABLED'] = True
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Carica configurazioni dell'email
app.config['MAIL_SERVER'] = EmailConfig.MAIL_SERVER
app.config['MAIL_PORT'] = EmailConfig.MAIL_PORT
app.config['MAIL_USERNAME'] = EmailConfig.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = EmailConfig.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = EmailConfig.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = EmailConfig.MAIL_USE_SSL
app.config['MAIL_DEFAULT_SENDER'] = EmailConfig.MAIL_DEFAULT_SENDER

# Initialize csrf
csrf = CSRFProtect(app)
# Initialize e-mail
mail = Mail(app)
# Initialize JWT and CORS
jwt = JWTManager(app)

# Abilita CORS per tutte le rotte
CORS(app)

# Initialize services
service_t_utenti = Service_t_utenti()
service_t_Log = Service_t_Log()
service_t_Reparti = Service_t_Reparti()
service_t_Servizi = Service_t_Servizi()
service_t_Alimenti = Service_t_Alimenti()
service_t_tipologiaalimenti = Service_t_tipologiaalimenti()
service_t_Allergeni = Service_t_Allergeni()
service_t_AssociazioneTipiPiattiTipiPreparazioni = Service_t_AssociazioneTipiPiattiTipiPreparazioni()
service_t_TipiPiatti= Service_t_TipiPiatti()
service_t_Piatti = Service_t_Piatti()
service_t_AssociazionePiattiPreparazionie = Service_t_AssociazionePiattiPreparazionie()
service_t_TipiMenu = Service_t_TipiMenu()
service_t_preparazioni = Service_t_preparazioni()
service_t_preparazionicontenuti = Service_t_preparazionicontenuti()
service_t_tipipreparazioni = Service_t_tipipreparazioni()
service_t_tipoquantita = Service_t_tipoquantita()
service_t_Menu = Service_t_Menu()
service_t_MenuServizi = Service_t_MenuServizi()
service_t_MenuServiziAssociazione = Service_t_MenuServiziAssociazione()
service_t_TipiAlimentazione = Service_t_TipiAlimentazione()
service_t_Schede = Service_t_Schede()
service_t_Ordini = Service_t_Ordini()
service_t_OrdiniSchede = Service_t_OrdiniSchede()
service_t_OrdiniPiatti = Service_t_OrdiniPiatti()
service_t_funzionalita = Service_t_funzionalita ()
service_t_SchedePiatti = Service_t_SchedePiatti()
service_t_tipiUtenti = Service_t_tipiUtenti()
service_t_FunzionalitaUtente = Service_t_FunzionalitaUtente()


# Define the blueprint
app_cucina = Blueprint('app_cucina', __name__, template_folder='template')

# Background job rimuve i token scaduti
def remove_expired_tokens():
    service_t_utenti.expiredTokens()

# Configura lo scheduler per rimuovere i token scaduti ogni minuto
scheduler = BackgroundScheduler()
#ogni 60 secondi fa il controllo
scheduler.add_job(func=remove_expired_tokens, trigger="interval", seconds=60)
scheduler.start()

# Gestisce i token scaduti
@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    user_id = jwt_payload['sub']
    service_t_utenti.do_logout(user_id)  # Disattiva l'utente
    session['authenticated'] = False
    response = jsonify({"message": "Logged out because the token has expired."})
    unset_jwt_cookies(response)
    return response


#-------------------------------------Funzioni--------------------------------------------


# Controlla se l'ora corrente è prima delle 14 ore rispetto alla data dell'ordine
def check_order_time_limit(order_date):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Blocca ordini per oggi o ieri
    if order_date <= today:
        return False

    # Controlla solo se l'ordine è per domani e dopo le 10 del mattino
    current_time = datetime.now().time()
    time_limit = datetime.strptime("10:00:00", "%H:%M:%S").time()

    if order_date == tomorrow and current_time > time_limit:
        return False

    return True


#struttura il percorso per i vari permessi
def get_page_name_from_path(path):
    # Rimuovi i caratteri di delimitazione finali e iniziali
    cleaned_path = path.strip('/')

    # Controlla se il percorso inizia con 'app_cucina/'
    if cleaned_path.startswith('app_cucina/'):
        # Rimuovi 'app_cucina/' dal percorso
        cleaned_path = cleaned_path[len('app_cucina/'):]
        
        # Trova il primo '/' dopo 'app_cucina/'
        first_slash_index = cleaned_path.find('/')
        
        # Restituisci il percorso fino al primo '/' includendo la barra
        if first_slash_index != -1:
            return '/' + 'app_cucina/' + cleaned_path[:first_slash_index]
        else:
            return '/' + 'app_cucina/' + cleaned_path

    # Se il percorso non inizia con 'app_cucina/', restituisci vuoto o il percorso originale
    return ''



def get_user_reparti(user_id):
    print(user_id)
    """
    Recupera la lista dei reparti accessibili da un determinato utente.

    :param user_id: ID dell'utente
    :return: Lista di reparti accessibili
    """
    # Ottieni la lista dei reparti per l'utente
    user_reparti_ids = service_t_utenti.get_reparti_list(user_id)
    
    # Se l'utente ha reparti associati, recupera solo quelli
    if user_reparti_ids:
        response = service_t_Reparti.get_by_ids(user_reparti_ids)
        if 'Error' in response:
            return {'Error': 'Errore nel recupero dei reparti'}
        return response['results']
    else:
        # Se non ci sono reparti associati, ritorna tutti i reparti
        return service_t_Reparti.get_all()


# Funzione per clonare un menu esistente
def clona_menu(menu_id, clone_date, utente_inserimento):
    try:
        # Funzione interna per ottenere i dati del menu
        def get_menu_data(menu_id):
            # Recupera le associazioni di piatti per il menu specificato
            assoc_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_id)
            # Recupera il menu stesso utilizzando il suo ID
            menu = service_t_MenuServizi.get_by_id(menu_id)
            # Recupera il tipo di menu associato
            tipo_menu = service_t_Menu.get_by_id(menu['fkMenu'])
            return assoc_piatti, menu, tipo_menu

        # Ottiene i dati del menu da clonare
        assoc_piatti, menu_da_clonare, tipo_menu_da_clonare = get_menu_data(menu_id)

        # Controlla se esiste già un menu con la data di clonazione e il tipo di menu specificato
        menu_by_data = service_t_Menu.get_by_data(clone_date, tipo_menu_da_clonare['fkTipoMenu'])

        # Se non esiste un menu con quella data, crea un nuovo menu
        if menu_by_data is None:
            new_menu_id = service_t_Menu.create(clone_date, tipo_menu_da_clonare['fkTipoMenu'], utenteInserimento=utente_inserimento)
            menu_by_data = service_t_Menu.get_by_id(new_menu_id)

        # Controlla che menu_by_data sia un dizionario
        if not isinstance(menu_by_data, dict):
            raise ValueError("Errore: menu_by_data dovrebbe essere un dizionario")

        # Recupera i servizi associati al menu clonabile
        menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(menu_by_data['id'], menu_da_clonare['fkServizio'])

        # Se non ci sono servizi associati, crea un nuovo servizio
        if menu_servizio is None:
            menu_servizio_id = service_t_MenuServizi.create(menu_by_data['id'], menu_da_clonare['fkServizio'], utenteInserimento=utente_inserimento)
            menu_servizio = service_t_MenuServizi.get_by_id(menu_servizio_id)
            # Verifica che menu_servizio sia un dizionario
            if not isinstance(menu_servizio, dict):
                raise ValueError("Errore: menu_servizio dovrebbe essere un dizionario")
        else:
            # Verifica che menu_servizio sia un dizionario
            if not isinstance(menu_servizio, dict):
                raise ValueError("Errore: menu_servizio dovrebbe essere un dizionario")

        # Log dei dati per debugging (da implementare se necessario)
       
        # Cancella le associazioni esistenti per il menu servizio
        service_t_MenuServiziAssociazione.delete_per_menu(menu_servizio['id'], utenteCancellazione=utente_inserimento)

        # Crea nuove associazioni per i piatti nel menu clonabile
        for associazione in assoc_piatti:
            service_t_MenuServiziAssociazione.create(menu_servizio['id'], associazione['id'], utenteInserimento=utente_inserimento)

        return True  # Clonazione avvenuta con successo

    except ValueError as ve:   
        # Gestione degli errori di validazione
        print(f"Errore di validazione: {str(ve)}")
        return False
    
    except Exception as e:
        # Gestione di altri errori durante la clonazione
        print(f"Errore durante la clonazione del menu: {str(e)}")
        return False



# Funzione che associa le preparazioni per ogni piatto considerando il tipo e il giorno del menu
def get_preparazioni_map(ordine_data, scheda_tipo_menu, servizio):
    # Recupera l'ID del menu corrispondente alla data dell'ordine e al tipo di menu
    id_menu = service_t_Menu.get_by_data(ordine_data, scheda_tipo_menu)
    
    # Controlla se si è verificato un errore nel recupero del menu
    if 'Error' in id_menu:
        print("Error retrieving menu:", id_menu)
        return {}  # Ritorna un dizionario vuoto in caso di errore

    # Recupera tutti i servizi associati al menu
    menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(id_menu['id'], servizio)
    
    # Verifica che il risultato di menu_servizio sia un dizionario e contenga un ID
    if isinstance(menu_servizio, dict) and 'id' in menu_servizio:
        # Recupera le associazioni di piatti per il servizio del menu
        menu_associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_servizio['id'])
        
        preparazioni_map = {}  # Inizializza un dizionario vuoto per le preparazioni

        # Itera attraverso le associazioni di piatti
        for assoc in menu_associazioni:
            # Controlla se l'associazione è un dizionario e contiene un ID
            if isinstance(assoc, dict) and 'id' in assoc:
                assoc_id = assoc['id']  # Ottiene l'ID dell'associazione
            else:
                assoc_id = assoc  # Presume che assoc sia già l'ID

            # Recupera le informazioni di associazione piatto-preparazione utilizzando l'ID
            fk_associazione_result = service_t_AssociazionePiattiPreparazionie.get_by_id(assoc_id)

            # Se il risultato è una tupla, ottiene il primo elemento
            if isinstance(fk_associazione_result, tuple):
                fk_associazione = fk_associazione_result[0]
            else:
                fk_associazione = fk_associazione_result  # Altrimenti, usa direttamente il risultato

            # Controlla se l'associazione di piatto-preparazione è valida e non contiene errori
            if fk_associazione and isinstance(fk_associazione, dict) and 'Error' not in fk_associazione:
                fk_piatto = fk_associazione['fkPiatto']  # Ottiene l'ID del piatto
                fk_preparazione = fk_associazione.get('fkPreparazione')  # Ottiene l'ID della preparazione
                
                
                # Usa la descrizione dalla mappa preparazioni se esiste, altrimenti recupera la descrizione dal servizio
                descrizione_preparazione = preparazioni_map.get(fk_piatto, service_t_preparazioni.get_descrizione_by_id(fk_preparazione))
                preparazioni_map[fk_piatto] = descrizione_preparazione  # Aggiorna la mappa con la descrizione del piatto
            else:
                print(f"Errore nella fk_associazione: {fk_associazione}")  # Stampa un messaggio di errore per il debug

        return preparazioni_map  # Ritorna la mappa delle preparazioni associate ai piatti
    else:
        return {}  # Ritorna un dizionario vuoto se non ci sono servizi associati

    
# funzione usata nel ordine personale per creare dinamicamente i menu e visualiuzare gli ordini fatti con i relativi piatti
def processa_ordine(data, nome, cognome, servizio_corrente, piatti, menu_personale):
    # Inizializza inf_scheda a None
    inf_scheda = None
    preparazioni_map = {}
    piatti_ordine = {}
    piatti_ordine_map = {}

    # Controlla l'ordine esistente
    controllo_ordine = service_t_OrdiniSchede.get_by_day_and_nome_cognome(data, nome, cognome, int(servizio_corrente))

    # Supponiamo che piatti_map e preparazioni_map siano già disponibili
    if controllo_ordine is not None:
        # Recupera tutti i piatti ordinati associati a quella scheda
        piatti_ordine = service_t_OrdiniPiatti.get_all_by_ordine_scheda(controllo_ordine['id'])
        
        
        # Ottieni le informazioni della scheda associata
        inf_scheda = service_t_Schede.get_by_id(controllo_ordine['fkScheda'])
        
        
        # Crea una mappa delle preparazioni in base al tipo di menu e al servizio
        preparazioni_map = get_preparazioni_map(data, inf_scheda['fkTipoMenu'], controllo_ordine['fkServizio'])
        
        
        # Crea una nuova mappa per i piatti ordinati
        piatti_ordine_map = {}
        
        # Itera attraverso i piatti ordinati e costruisci la mappa con codice e preparazione
        for piatto_ordine in piatti_ordine:
            piatto_id = int(piatto_ordine['fkPiatto'])
            
            
            p_m = {int(piatto['id']): {'titolo': piatto['titolo'], 'codice': piatto['codice'], 'fkTipoPiatto': piatto['fkTipoPiatto']} for piatto in piatti}
            # Verifica se il piatto esiste in piatti_map
            if piatto_id in p_m:
                
                
                # Aggiungi il piatto alla mappa dei piatti ordinati con i dettagli necessari
                piatti_ordine_map[piatto_ordine['id']] = {
                    'id': piatto_ordine['id'],
                    'fkPiatto': piatto_ordine['fkPiatto'],
                    'quantita': piatto_ordine['quantita'],
                    'note': piatto_ordine['note'],
                    'titolo': preparazioni_map.get(piatto_id, p_m[piatto_id]['titolo']),  # Usa la descrizione della preparazione
                    'codice': p_m[piatto_id]['codice'],  # Usa il codice del piatto
                    'fkTipoPiatto': p_m[piatto_id]['fkTipoPiatto']  # Tipo di piatto (es. primo, secondo, etc.)
                }
            else:
                print(f"Piatto con ID {piatto_id} non trovato in piatti_map.")
        
        
        
        return controllo_ordine, inf_scheda, preparazioni_map, piatti_ordine_map
    
    else:
        # Se non esiste l'ordine, costruisci il menu personale
        for scheda in menu_personale:
            preparazioni_map = get_preparazioni_map(data, scheda['fkTipoMenu'], int(servizio_corrente))
            
            piatti_map = {}
            for piatto in piatti:
                piatto_id = int(piatto['id'])
                
                # Filtra solo i piatti (preparazioni) che fanno parte del menu
                if piatto_id in preparazioni_map:
                    piatti_map[piatto_id] = {
                        'id': piatto['id'],
                        'titolo': preparazioni_map.get(piatto_id),  # Usa solo la descrizione della preparazione
                        'codice': piatto['codice'],
                        'fkTipoPiatto': piatto['fkTipoPiatto']
                    }

            # Assegna piatti_map alla scheda corrente
            scheda['piatti'] = piatti_map
        
        return None, None, preparazioni_map, menu_personale


#-------------------------------------------------INIZIO PRE-CHIAMATE API------------------------------------------


@app_cucina.before_request
def check_token_and_permissions():
    """
    Controlla l'autenticazione e i permessi dell'utente prima di gestire una richiesta.

    Questa funzione consente di:
    - Verificare se l'utente è autenticato e se ha i permessi necessari per accedere alle rotte protette.
    - Gestire la validità del token dell'utente, reindirizzando alla pagina di login se non autenticato o se il token è scaduto.

    La funzione esegue le seguenti operazioni per ogni richiesta ricevuta:
    - Verifica se la rotta corrente è esente dai controlli di autenticazione.
    - Se l'utente non è autenticato, reindirizza alla pagina di login.
    - Controlla la validità del token dell'utente e lo aggiorna, se necessario.
    - Verifica i permessi dell'utente per accedere alla pagina richiesta.

    Args:
        Nessuno. Le informazioni di autenticazione e permesso sono gestite attraverso la sessione.

    Returns:
        Response:
            - Se l'utente non è autenticato o il token non è valido, viene reindirizzato alla pagina di login.
            - Se l'utente non ha i permessi per accedere alla pagina richiesta, viene generato un errore 403.
            - In caso di errori durante il processo, viene generato un errore 500.

    Notes:
        - Le rotte esenti dal controllo di autenticazione e permessi sono definite in `exempt_routes`.
        - La funzione utilizza i servizi `service_t_utenti` e `service_t_funzionalita` per gestire la validità del token e i permessi.
        - Eventuali errori durante la verifica vengono registrati nel log per facilitare il debug.
        - La scadenza del token viene gestita e impostata a 30 minuti dalla sua ultima validazione.
    """

    # Definisce le rotte esenti dal controllo di autenticazione e permessi
    exempt_routes = ['app_cucina.login', 
                     'app_cucina.index',
                     'app_cucina.reset_password', 
                     'app_cucina.richiesta_recupero_password', 
                     'app_cucina.do_logout', 
                     'app_cucina.contatti'
                     ]

    # Controlla se la rotta attuale è esente dal controllo
    if request.endpoint in exempt_routes:
        return  # Non esegue ulteriori controlli se la rotta è esente

    # Verifica se l'utente è autenticato
    if 'authenticated' not in session or not session.get('authenticated'):
        return redirect(url_for('app_cucina.login'))  # Reindirizza al login se non autenticato

    try:
        # Recupera l'ID utente dalla sessione
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('app_cucina.login'))  # Reindirizza al login se non presente l'ID utente

        # Recupera il token dalla sessione
        token = session.get('token')
        # Verifica la validità del token
        is_token_valid = service_t_utenti.is_token_valid(user_id, token)

        if not is_token_valid:
            # Se il token è scaduto, gestisce l'espulsione e pulisce la sessione
            service_t_utenti.expiredTokens()
            session.clear()
            return redirect(url_for('app_cucina.login'))  # Reindirizza al login

        # Gestisce il token e lo aggiorna nella sessione
        response = service_t_utenti.manage_token(user_id, token)
        if response and 'token' in response.json:
            session['token'] = response.json['token']  # Aggiorna il token nella sessione
            expires = datetime.now() + timedelta(minutes=30)  # Imposta la scadenza del token
            session['expires'] = expires  # Salva la scadenza nella sessione
            
    except Exception as e:
        # Cattura e registra eventuali errori durante la verifica del token
        logging.error(f"Error verifying token for user_id {user_id}: {str(e)}")
        session.clear()  # Pulisce la sessione in caso di errore
        abort(500)  # Lancia un errore 500 in caso di errore critico

    try:
        # Recupera il tipo di utente dalla sessione
        user_type_id = session.get('fkTipoUtente')
        # Ottiene il link della pagina attuale
        page_link = get_page_name_from_path(request.path)

        # Verifica se l'utente ha accesso alla pagina richiesta
        access_granted, message = service_t_funzionalita.can_access(user_type_id=user_type_id, page_link=page_link)

        if not access_granted:
            # Se l'accesso non è consentito, registra l'evento e lancia un errore 403
            logging.warning(f"Access denied for user_id {user_id} to {page_link}: {message}")
            abort(403)  # Lancia un errore 403 per accesso negato
            
    except Exception as e:
        # Cattura gli errori relativi al controllo dei permessi
        logging.error(f"Error checking permissions for user_id {user_id}: {str(e)}")
        abort(500)  # Lancia un errore 500 in caso di problemi imprevisti


@app_cucina.before_request
def check_csrf():
    """
    Controlla la protezione CSRF (Cross-Site Request Forgery) per le richieste ricevute.

    Questa funzione consente di:
    - Applicare la protezione CSRF a tutte le rotte, eccetto quelle specificate come esenti.

    """
    exempt_routes = ['app_cucina.login',
                     'app_cucina.index',
                     'app_cucina.do_logout',
                     'app_cucina.reset_password',
                     'app_cucina.richiesta_recupero_password',
                     'app_cucina.contatti' ]
    if request.endpoint not in exempt_routes:
        csrf.protect()


#logga le richieste degli utente ma solo le richieste ('POST', 'PUT', 'DELETE')
@app.before_request
def log_request_info():
    if request.method in ['POST', 'PUT', 'DELETE']:
        # Verifica se il percorso è esente dal logging
        if request.path in ['/app_cucina/login']:
            return  # Salta il logging per queste chiamate

        # Recupera l'ID utente e lo username direttamente dalla sessione
        fkUser = session.get('username', None)

        # Ottieni i dati della richiesta
        data = request.json if request.is_json else request.form.to_dict()

        # Log iniziale
        service_t_Log.log_to_db(
            level='INFO',
            message=f'{request.method} request to {request.path}.',
            fkUser=fkUser,
            route=request.path,
            data=data
        )
#logga le risposte del server ma solo le richieste ('POST', 'PUT', 'DELETE')
@app.after_request
def log_request_success(response):
    if request.method in ['POST', 'PUT', 'DELETE'] and response.status_code == 200:
        # Verifica se il percorso è esente dal logging
        if request.path in ['/app_cucina/login']:
            return response  # Salta il logging per queste chiamate

        # Recupera l'ID utente e lo username dalla sessione
        fkUser = session.get('username', None)

        # Log del successo dell'operazione
        service_t_Log.log_to_db(
            level='INFO',
            message=f'{request.method} request to {request.path}.',
            fkUser=fkUser,
            route=request.path,
            data=None
        )
    return response
#logga gli errori 
@app.teardown_request
def log_request_error(error):
    if error:
        # Recupera l'ID utente e lo username dalla sessione
        fkUser = session.get('username', None)
       
        # Verifica se il percorso è esente dal logging
        if request.path in ['/app_cucina/login']:
            return  # Salta il logging per queste chiamate

        # Se c'è un errore, logga l'errore
        service_t_Log.log_to_db(
            level='ERROR',
            message=f'Error during {request.method} request to {request.path}: {str(error)}',
            fkUser=fkUser,
            route=request.path,
            data=request.json if request.is_json else request.form.to_dict()
        )
    return error


#-------------------------------------------------INIZIO CHIAMATE API---------------------------------------



#prima pagina che porta al login
@app_cucina.route('/')
def pagina_iniziale():
    return redirect(url_for('login'))



@app_cucina.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestisce l'autenticazione degli utenti attraverso il login.

    Questa funzione consente di:
    - Fornire un'interfaccia per l'inserimento delle credenziali dell'utente.
    - Validare le credenziali fornite e gestire la sessione dell'utente autenticato.
    - Reindirizzare l'utente a una pagina specificata dopo un accesso riuscito.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Visualizza il modulo di login.
    - **POST**: Valida le credenziali dell'utente e, se valide, autentica l'utente e avvia una sessione.

    Args:
        Nessuno. Le informazioni di login sono gestite attraverso il modulo `LoginFormNoCSRF`.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'loginx.html' con il modulo di login.
            - **POST**:
                - Se le credenziali sono valide:
                    - Autentica l'utente e memorizza i dati della sessione, inclusi ID utente, token e tipo di utente.
                    - Reindirizza l'utente alla home page dell'applicazione.
                - Se le credenziali non sono valide:
                    - Mostra un messaggio di errore e riporta l'utente alla pagina di login.

    Notes:
        - Se si verifica un errore durante il processo di login, vengono visualizati messaggi specifici a seconda dell'errore:
            -Gestione dell'eccezione se l'utente non esiste.
            -Gestione dell'eccezione se la password è sbagliata o l'utente è scaduto.
            -Gestione generica per eventuali altri errori.
        - Le credenziali sono validate utilizzando il servizio `service_t_utenti` che gestisce l'autenticazione.
        - Il sistema mantiene la struttura del menu dell'utente autenticato per l'accesso rapido alle funzionalità.
        - È previsto l'uso di un modulo senza protezione CSRF per consentire la gestione delle richieste di login.
    """

    
    form = LoginFormNoCSRF()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            # Chiama il servizio per eseguire il login
            user = service_t_utenti.do_login(username, password)  

            if user:
                # Setta i dati della sessione
                session['authenticated'] = True
                session['user_id'] = user['public_id']
                session['token'] = user['token']
                session['fkTipoUtente'] = user['fkTipoUtente']
                session['username'] = user['username']

                # Costruisci il menu di navigazione
                menu_structure = service_t_FunzionalitaUtente.build_menu_structure(user['public_id'])
                session['menu_structure'] = menu_structure

                return redirect(url_for('app_cucina.home'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('loginx.html', form=form)

        except NotFound as e:
            # Gestione dell'eccezione se l'utente non esiste
            flash(str(e), 'error')
            return render_template('loginx.html', form=form)

        except Forbidden as e:
            # Gestione dell'eccezione se la password è sbagliata o l'utente è scaduto
            flash(str(e), 'error')
            return render_template('loginx.html', form=form)

        except Exception as e:
            # Gestione generica per eventuali altri errori
            print(f"Error during login: {e}")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('loginx.html', form=form)

    return render_template('loginx.html', form=form)  # GET request



@app_cucina.context_processor
def inject_user_data():

    """
    Inietta dati utente e struttura del menu nei template dell'applicazione.

    Questa funzione consente di:
    - Recuperare informazioni relative alla sessione dell'utente, inclusi menu e permessi.
    - Fornire i dati necessari per il rendering delle pagine, garantendo che le informazioni siano disponibili nei template.

    La funzione esegue le seguenti operazioni:
    - Recupera la struttura del menu, il tipo di utente e il token dalla sessione.
    - Per ogni pagina nella struttura del menu, controlla i permessi di accesso e scrittura.
    - Gestisce anche i permessi per eventuali sotto-pagine e nipoti nella struttura del menu.

    Returns:
        dict: Un dizionario con i seguenti dati accessibili nei template:
            - menu_structure (list): La struttura del menu recuperata dalla sessione.
            - username (str): Il nome utente attualmente autenticato.
            - token (str): Il token di autenticazione dell'utente.
            - user_type (int): Il tipo di utente, recuperato dalla sessione.
            - form (LogoutFormNoCSRF): Un modulo per il logout senza protezione CSRF.
            - current_page_link (str): Il link della pagina attualmente visualizzata.
            - page_permissions (dict): Un dizionario dei permessi per ciascuna pagina nel menu, con chiavi per 'can_write'.

    Notes:
        - I permessi di scrittura vengono determinati in base ai valori forniti dal servizio `service_t_funzionalita`.
        - La funzione assicura che i template abbiano accesso a tutte le informazioni necessarie per gestire la visualizzazione e le funzionalità in base ai permessi dell'utente.
        - Viene utilizzata per controllare l'accesso alle varie sezioni dell'applicazione in base al tipo di utente.
    """
    menu_structure = session.get('menu_structure', [])
    user_type = session.get('fkTipoUtente')
    token = session.get('token')

    # Prepara i permessi per le pagine presenti nella struttura del menu
    page_permissions = {}
    for page in menu_structure:
        # Controlla i permessi per la pagina principale
        access_granted, permessi = service_t_funzionalita.can_access(user_type_id=user_type, page_link=page['link'])
        
        # Gestisce se l'utente ha permessi di scrittura o solo lettura
        can_write = bool(permessi)  # Verifica se permessi è 1 (scrittura), altrimenti è False (sola lettura)
        page_permissions[page['link']] = {
            'can_write': can_write,  # True se può scrivere, altrimenti False
        }

        # Se ci sono sotto-pagine, verifica i permessi anche per queste
        for child in page.get('figli', []):
            access_granted, permessi = service_t_funzionalita.can_access(user_type_id=user_type, page_link=child['link'])
            can_write = bool(permessi)
            page_permissions[child['link']] = {
                'can_write': can_write,
            }

            # Se ci sono nipoti, verifica anche i permessi
            for grandchild in child.get('nipoti', []):
                access_granted, permessi = service_t_funzionalita.can_access(user_type_id=user_type, page_link=grandchild['link'])
                can_write = bool(permessi)
                page_permissions[grandchild['link']] = {
                    'can_write': can_write,
                }


    # Ritorna i dati che devono essere accessibili nei template
    return dict(
        menu_structure=menu_structure,
        username=session.get('username'),
        token=token,
        form=LogoutFormNoCSRF(),
        user_type=user_type,
        current_page_link=request.path,
        page_permissions=page_permissions  # Aggiungi i permessi delle pagine
    )


#crea indice 
@app_cucina.route('/index')
def index():
    if 'authenticated' in session:       
        return render_template('index.html')
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/home', methods=['GET', 'POST'])
def home():
    """
    Gestisce la visualizzazione della pagina principale per gli utenti autenticati.

    Questa funzione consente di:
    - Visualizzare le informazioni quotidiane relative agli ordini, compresi i totali per servizio.
    - Recuperare i dettagli dell'utente autenticato e dei servizi disponibili.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza le informazioni relative agli ordini per il giorno specificato.
    - **POST**: Attualmente non supporta la creazione o la modifica di dati, ma potrebbe essere esteso in futuro.

    Args:
        Nessuno. Le informazioni sul giorno, i servizi e gli ordini sono gestite attraverso le query string e i dati di sessione.

    Query Parameters:
        year (int, optional): L'anno da visualizzare (default è l'anno corrente).
        month (int, optional): Il mese da visualizzare (default è il mese corrente).
        day (int, optional): Il giorno da visualizzare (default è il giorno corrente).

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'home.html' con i seguenti dati:
                    - Informazioni sugli ordini totali per servizio per la data specificata.
                    - Totale pazienti e personale per il giorno selezionato.
                    - Dettagli dei piatti e dei servizi disponibili.
                    - Controllo degli ordini associati all'utente.
                    - Informazioni personali dell'utente autenticato, inclusi nome e cognome.
                    - Mappa dei servizi disponibili e tipi di menu.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come ordini, piatti, e dettagli dell'utente.
        - Viene calcolato il totale degli ordini per ogni servizio per il giorno specificato.
        - La funzione gestisce anche il caso in cui non siano presenti ordini per il giorno e il servizio specificati, restituendo un valore di controllo appropriato.
    """ 
    if 'authenticated' in session:
        try:
             # Ottieni la data di domani
            tomorrow = datetime.now().date() + timedelta(days=1)  
            year = request.args.get('year', tomorrow.year, type=int)
            month = request.args.get('month', tomorrow.month, type=int)
            day = request.args.get('day', tomorrow.day, type=int)
            servizi = service_t_Servizi.get_all_servizi()
            ultimi_menu = service_t_Menu.get_latest_by_fkTipoMenu()
            user = service_t_utenti.get_utente_by_public_id(session['user_id'])
            
            # Calcola il mese e l'anno precedente
            mese_scorso_data = tomorrow - relativedelta(months=1)
            mese_scorso = mese_scorso_data.month
            anno_mese_scorso = mese_scorso_data.year

            # Definisci i dati utente
            data = f'{year}-{month}-{day}'
            nome = user['nome']
            cognome = user['cognome']

            # Dizionario per accumulare i risultati
            ordini_totali_per_servizio = {}
            
            ordini_totali_mese_corrente_per_servizio = {}
            
            ordini_totali_mese_scorso_per_servizio = {}
            ordini_totali_anno_per_servizio = {}

            # Utilizza il metodo del service per calcolare i totali
            ordini_totali_per_servizio, totale_pazienti, totale_personale, totale_completo = \
                service_t_OrdiniSchede.calcola_totali_per_giorno(data, servizi)

            ordini_totali_mese_corrente_per_servizio, totale_mese_corrente_completo = \
                service_t_OrdiniSchede.calcola_totali_per_mese(mese=month, anno=year, servizi=servizi)

            ordini_totali_mese_scorso_per_servizio, totale_mese_scorso_completo = \
                service_t_OrdiniSchede.calcola_totali_per_mese(mese=mese_scorso, anno=anno_mese_scorso, servizi=servizi)

            ordini_totali_anno_per_servizio, totale_anno_completo = \
                service_t_OrdiniSchede.calcola_totali_per_anno(anno=year, servizi=servizi)

            ordini_per_menu_anno = service_t_OrdiniSchede.count_totali_tipo_menu(anno=year)

            ordini_per_menu_mese = service_t_OrdiniSchede.count_totali_tipo_menu(anno=year, mese=month)

            ordini_per_menu_giorno = service_t_OrdiniSchede.count_totali_tipo_menu(anno=year, mese=month, giorno=day)




            piatti = service_t_Piatti.get_all()
            menu_personale = service_t_Schede.get_all_personale()
            tipi_menu = service_t_TipiMenu.get_all()
            
            # Crea mappe per descrizioni e colori dei tipi di menu
            tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
            tipi_menu_colore = {int(tipo_menu['id']): tipo_menu['backgroundColor'] for tipo_menu in tipi_menu}
            servizi_map = {int(servizio['id']): servizio['descrizione'] for servizio in servizi}

            dizionario_servizi = {}

            for servizio in servizi:
                controllo_ordine, inf_scheda, preparazioni_map, piatti_ordine_map = processa_ordine(
                    data, nome, cognome, servizio['id'], piatti, menu_personale
                )
                
                # Gestione del caso in cui controllo_ordine è None
                dizionario_servizi[servizio['id']] = {
                    'inf_scheda': inf_scheda,
                    'piatti_ordine_map': piatti_ordine_map,
                    'controllo_ordine': controllo_ordine if controllo_ordine else 'Null'
                }

            # Rendering della template con i dati calcolati
            return render_template(
                'home.html',
                year=year,
                month=month,
                day=day,
                ultimi_menu=ultimi_menu,
                servizi=servizi,
                controllo_ordine=controllo_ordine, 
                inf_scheda=inf_scheda,                                                     
                piatti_ordine_map=piatti_ordine_map, 
                utente=user['username'],
                nome=nome,
                cognome=cognome,
                servizi_map=servizi_map,
                dizionario_servizi=dizionario_servizi,
                tipi_menu_map=tipi_menu_map,
                tipi_menu_colore=tipi_menu_colore,
                ordini_per_menu_anno=ordini_per_menu_anno,
                ordini_per_menu_mese=ordini_per_menu_mese,
                ordini_per_menu_giorno=ordini_per_menu_giorno,
                tomorrow=tomorrow,

                ordini_totali_per_servizio=ordini_totali_per_servizio,
                totale_pazienti=totale_pazienti or 0,
                totale_personale=totale_personale or 0,
                totale_completo=totale_completo or 0,
                
                ordini_totali_mese_corrente_per_servizio=ordini_totali_mese_corrente_per_servizio,
                totale_mese_corrente_completo=totale_mese_corrente_completo or 0,

                ordini_totali_mese_scorso_per_servizio=ordini_totali_mese_scorso_per_servizio,
                totale_mese_scorso_completo=totale_mese_scorso_completo or 0,

                ordini_totali_anno_per_servizio=ordini_totali_anno_per_servizio,
                totale_anno_completo=totale_anno_completo or 0
            )

        except Exception as e:
            # Gestione degli errori imprevisti
            print(f"Errore: {e}")
            return redirect(url_for('app_cucina.login'))

    else:
        return redirect(url_for('app_cucina.login'))




@app_cucina.route('/alimenti', methods=['GET', 'POST'])
def alimenti():
    """
    Gestisce la visualizzazione e la creazione di alimenti nel sistema.

    Questa funzione consente di:
    - Visualizzare un elenco di alimenti già esistenti.
    - Creare un nuovo alimento specificando le sue caratteristiche e i suoi allergeni.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza l'elenco degli alimenti, le tipologie disponibili e gli allergeni.
    - **POST**: Crea un nuovo alimento se il modulo viene inviato con dati validi.

    Args:
        Nessuno. Le informazioni sugli alimenti, le tipologie e gli allergeni sono gestite attraverso i servizi.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'alimenti.html' con i seguenti dati:
                    - Elenco degli alimenti esistenti.
                    - Lista delle tipologie di alimenti.
                    - Lista degli allergeni.
                    - Mappa delle tipologie e degli allergeni per un accesso facile.
                    - Form per inserire un nuovo alimento.
            - **POST**:
                - Se il modulo è valido, viene creato un nuovo alimento con le informazioni specificate.
                - Ritorna alla pagina aggiornata degli alimenti con un messaggio di successo.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati da un database, inclusi alimenti, tipologie e allergeni.
        - Il form per l'aggiunta di un alimento consente di specificare allergeni multipli e tipologie.
        - Un messaggio di successo viene mostrato dopo l'aggiunta di un nuovo alimento.
    """
    if 'authenticated' in session:


        # Retrieve the list of alimenti, tipologie, and allergeni from your database
        alimenti_list = service_t_Alimenti.get_all()
        tipologie = service_t_tipologiaalimenti.get_all_tipologiaalimenti()
        allergeni = service_t_Allergeni.get_all()
        
        # Create maps for tipologie and allergeni
        tipologie_map = {int(tipologia['id']): tipologia['nome'] for tipologia in tipologie}
        allergeni_map = {str(allergene['id']): allergene['nome'] for allergene in allergeni}

        form = AlimentiForm()
        form.fkAllergene.choices = [(allergene['id'], allergene['nome']) for allergene in allergeni]
        form.fkTipologiaAlimento.choices = [(tipologia['id'], tipologia['nome']) for tipologia in tipologie]

    
        if form.validate_on_submit():
            fkAllergene = ",".join(str(allergene_id) for allergene_id in form.fkAllergene.data)

            service_t_Alimenti.create(
                alimento=form.alimento.data,
                energia_Kcal=form.energia_Kcal.data,
                energia_KJ=form.energia_KJ.data,
                prot_tot_gr=form.prot_tot_gr.data,
                glucidi_tot=form.glucidi_tot.data,
                lipidi_tot=form.lipidi_tot.data,
                saturi_tot=form.saturi_tot.data,
                fkAllergene=fkAllergene,
                fkTipologiaAlimento=form.fkTipologiaAlimento.data
            )

            flash('Alimento aggiunto con successo!', 'success')
            return redirect(url_for('app_cucina.alimenti'))
            

        return render_template(
            'alimenti.html',
            alimenti=alimenti_list,
            tipologie=tipologie,
            allergeni=allergeni,
            tipologie_map=tipologie_map,
            allergeni_map=allergeni_map,
            form=form
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/alimenti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_alimento(id):
    
    if 'authenticated' in session:

        if request.method == 'GET':
            alimento = service_t_Alimenti.get_by_id(id)
            tipologie = service_t_tipologiaalimenti.get_all_tipologiaalimenti()
            allergeni = service_t_Allergeni.get_all()

            form = AlimentiForm(obj=alimento)
            form.fkAllergene.choices = [(allergene['id'], allergene['nome']) for allergene in allergeni]
            form.fkTipologiaAlimento.choices = [(tipologia['id'], tipologia['nome']) for tipologia in tipologie]
            
            if alimento:
                alim_json = jsonify({
                    'alimento': alimento.get('alimento'),
                    'energia_Kcal': alimento.get('energia_Kcal'),
                    'energia_KJ': alimento.get('energia_KJ'),
                    'prot_tot_gr': alimento.get('prot_tot_gr'),
                    'glucidi_tot': alimento.get('glucidi_tot'),
                    'lipidi_tot': alimento.get('lipidi_tot'),
                    'saturi_tot': alimento.get('saturi_tot'),
                    'fkAllergene': alimento.get('fkAllergene'),
                    'fkTipologiaAlimento': alimento.get('fkTipologiaAlimento'),
                })
                return alim_json
            else:
                return jsonify({'error': 'Alimento non trovato.'}), 404

        if request.method == 'PUT':
            print("Richiesta PUT ricevuta")
            alimento = service_t_Alimenti.get_by_id(id)
            if not alimento:
                return jsonify({'error': 'Alimento non trovato.'}), 404

            form = AlimentiForm(request.form)

            try:
                # Crea la stringa fkAllergene
                fkAllergene = ",".join(str(allergene_id) for allergene_id in form.fkAllergene.data)

                # Esegui l'aggiornamento
                service_t_Alimenti.update(
                    id=id,    
                    alimento=form.alimento.data,
                    energia_Kcal=form.energia_Kcal.data,
                    energia_KJ=form.energia_KJ.data,
                    prot_tot_gr=form.prot_tot_gr.data,
                    glucidi_tot=form.glucidi_tot.data,
                    lipidi_tot=form.lipidi_tot.data,
                    saturi_tot=form.saturi_tot.data,
                    fkAllergene=fkAllergene,
                    fkTipologiaAlimento=form.fkTipologiaAlimento.data
                )

                return jsonify({'message': 'Piatto aggiornato con successo!'}), 200

            except Exception as e:
                print(f"Errore durante l'aggiornamento: {e}")
                return jsonify({'error': 'Errore durante l\'aggiornamento del Servizio'}), 500
            

        if request.method == 'DELETE':
            alimento = service_t_Alimenti.get_by_id(id)
            if not alimento:
                return jsonify({'error': 'Alimento non trovato.'}), 404
            try:
                service_t_Alimenti.delete(id=id)
                return jsonify({'message': f'Alimento {id} eliminato con successo!'}), 204
            except Exception as e:
                print(f"Errore durante l'eliminazione: {e}")
                return jsonify({'error': 'Errore durante l\'eliminazione del Servizio'}), 400
    else:
        return redirect(url_for('app_cucina.login'))




@app_cucina.route('/preparazioni', methods=['GET', 'POST'])
def preparazioni():
    """
    Gestisce la visualizzazione e la creazione di preparazioni culinarie.

    Questa funzione consente di:
    - Visualizzare l'elenco delle preparazioni esistenti.
    - Creare una nuova preparazione con relativi ingredienti e associazioni ai piatti.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutte le preparazioni, i tipi di preparazione, gli alimenti e i tipi di quantità.
    - **POST**: Crea una nuova preparazione e associa gli ingredienti specificati.

    Args:
        Nessuno. Le informazioni sulle preparazioni, gli alimenti e i tipi di preparazione sono gestite attraverso i dati recuperati dai servizi e dai moduli.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'preparazioni.html' con i seguenti dati:
                    - Elenco delle preparazioni esistenti.
                    - Elenco dei tipi di preparazione disponibili.
                    - Elenco degli alimenti disponibili.
                    - Elenco dei tipi di quantità disponibili.
                    - Moduli per inserire nuove preparazioni e ingredienti.
            - **POST**:
                - Se il modulo di preparazione è valido, viene creata una nuova preparazione e associati gli ingredienti specificati.
                - Reindirizza alla pagina aggiornata delle preparazioni con un messaggio di successo.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come preparazioni, tipi di preparazione, alimenti, e tipi di quantità.
        - La gestione del caricamento delle immagini è inclusa nel processo di creazione delle preparazioni.
        - Gli ingredienti della preparazione sono gestiti come una lista JSON che viene elaborata e salvata nel database.
    """
    if 'authenticated' in session:
        #FACCIAMO TUTTE LE GET CHE CI SEERVONO
        preparazioni = service_t_preparazioni.get_all_preparazioni()#recupera tutte le preparazioni
        tipiPreparazioni = service_t_tipipreparazioni.get_all_tipipreparazioni()#recupera tutti i tipiPreparazioni
        preparazioniContenuti = service_t_preparazionicontenuti.get_all_preparazioni_contenuti()#recupera tutti i preparazioniContenuti
        piatti = service_t_Piatti.get_all()#recupera tutti i piatti
        alimenti = service_t_Alimenti.get_all()#recupera tutti gli alimenti
        tipi_quantita = service_t_tipoquantita.get_all_tipoquantita()#recupera tutti i tipi_quantita
        preparazioni_base = service_t_preparazioni.get_all_preparazioni_base()#recupera tutte le preparazioni_base
        #recupera tutte le preparazioni base base senza ingredienti così da segnalarle nel front end
        preparazioni_senza_ingredienti = service_t_preparazionicontenuti.get_preparazioni_senza_ingredienti()
        

            
        #ISTANZIAMO LE FORM PER COSTRUIRE I FORM NEL HTML
        piattiform = PiattiForm()
        form = PreparazioniForm()
        alimform = AlimentoForm()

        # Popoliamo le scelte per il campo del tipo di preparazione nel modulo
        form.fkTipoPreparazione.choices = [
            (tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni
        ]

        # Popoliamo le scelte per il campo dell'alimento nel modulo alimform
        alimform.fkAlimento.choices = [
            (alimento['id'], alimento['alimento']) for alimento in alimenti  # Aggiungiamo tutti gli alimenti
        ] + [
            (preparazione['id'] + 100000, preparazione['descrizione']) for preparazione in preparazioni_base  # Aggiungiamo le preparazioni base con un offset unico per l'ID
        ]

        # Popoliamo le scelte per il campo del tipo di quantità nel modulo alimform
        alimform.fkTipoQuantita.choices = [
            (tipo_quantita['id'], tipo_quantita['tipo']) for tipo_quantita in tipi_quantita  # Aggiungiamo tutti i tipi di quantità
        ]


        TipoPreparazione_map = {int(tipoPreparazione['id']): tipoPreparazione['descrizione'] for tipoPreparazione in tipiPreparazioni}
        alimento_map = {int(alimento['id']): alimento['alimento'] for alimento in alimenti}
        tipo_map = {int(tipo_quantita['id']): tipo_quantita['tipo'] for tipo_quantita in tipi_quantita}
        
    
        if form.validate_on_submit():
            # Handling the image upload
            if form.immagine.data:
                image_filename = secure_filename(form.immagine.data.filename)
                form.immagine.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            else:
                image_filename = None

            
            fk_piatto = request.form.get('titolo')


            # Create the preparation record and get its ID
            new_preparazione_id = service_t_preparazioni.create_preparazione(
                
                fkTipoPreparazione=form.fkTipoPreparazione.data, 
                descrizione=form.descrizione.data, 
                isEstivo=form.isEstivo.data, 
                isInvernale=form.isInvernale.data,  
                inizio=form.inizio.data if form.inizio.data else None, 
                fine=form.fine.data if form.fine.data else None,  
                utenteInserimento=session.get('username'), 
                immagine=image_filename
            )

            service_t_AssociazionePiattiPreparazionie.create(
                fkPiatto=fk_piatto, 
                fkPreparazione = new_preparazione_id,
                utenteInserimento = session.get('username')
            )       

            ingredient_list = json.loads(request.form['ingredientList'])

            for ingredient in ingredient_list:
                try:
                    # Save ingredient
                    service_t_preparazionicontenuti.create_preparazioni_contenuti(
                        fkPreparazione=new_preparazione_id,
                        fkAlimento=int(ingredient['fkAlimento']),
                        quantita=float(ingredient['quantita']),  # Ensure this is a float
                        fkTipoQuantita=int(ingredient['fkTipoQuantita']),
                        note=ingredient['note'],
                        utenteInserimento=session.get('username')
                    )
                except (ValueError, KeyError) as e:
                    print(f"Error processing ingredient: {ingredient}, error: {e}")

            flash('Preparazione aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.preparazioni'))  # Redirect to the list of preparations


        return render_template(
            'preparazioni.html',
            preparazioni=preparazioni,
            tipiPreparazioni=tipiPreparazioni,
            preparazioniContenuti=preparazioniContenuti,
            tipiQuantia=tipi_quantita,
            TipoPreparazione_map=TipoPreparazione_map,
            form=form,
            alimenti=alimenti,
            tipi_quantita=tipi_quantita,
            alimform=alimform,
            alimento_map=alimento_map,
            piattiform=piattiform,
            piatti=piatti,
            tipo_map=tipo_map,
            preparazioni_base =preparazioni_base,
            preparazioni_senza_ingredienti=preparazioni_senza_ingredienti

        )
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/preparazioni/<int:id_preparazione>', methods=['GET', 'POST', 'DELETE'])
def preparazione_dettagli(id_preparazione):
    """
    Gestisce i dettagli di una preparazione specifica, inclusa la visualizzazione, modifica ed eliminazione.

    Questa funzione consente di:
    - Visualizzare i dettagli di una preparazione esistente.
    - Modificare le informazioni relative a una preparazione specifica.
    - Eliminare una preparazione esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera i dettagli della preparazione specificata dall'ID e restituisce i dati in formato JSON.
    - **POST**: Aggiorna i dettagli della preparazione con i dati forniti nel form.
    - **DELETE**: Rimuove la preparazione specificata dall'ID.

    Args:
        id_preparazione (int): L'ID della preparazione da gestire.

    Returns:
        Response:
            - **GET**:
                - Restituisce un JSON contenente:
                    - Dettagli della preparazione, inclusi tipo, descrizione, stato estivo/invernale e date di inizio e fine.
                    - Lista degli ingredienti associati alla preparazione.
                    - Scelte disponibili per tipi di preparazione, alimenti e quantità.
            - **POST**:
                - Se la modifica è avvenuta con successo, reindirizza alla lista delle preparazioni.
                - In caso di errore, mostra un messaggio di errore e reindirizza alla lista delle preparazioni.
            - **DELETE**:
                - Se la preparazione è stata eliminata con successo, restituisce un codice di stato 204 (No Content).
                - In caso di errore, restituisce un codice di stato 400 (Bad Request) con un messaggio di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza diversi servizi per recuperare e gestire i dati delle preparazioni e degli ingredienti associati.
        - La funzione gestisce anche l'associazione di piatti e il contenuto delle preparazioni per una corretta manipolazione dei dati.
        - Per la modifica, la funzione si aspetta che i dati degli ingredienti siano forniti come una lista JSON nel campo 'ingredientList' del form.
    """ 
    if 'authenticated' in session:
        
        if request.method == 'GET':
            # Recupera la preparazione basata sull'ID fornito
            preparazione = service_t_preparazioni.get_preparazione_by_id(id_preparazione)
            
            if not preparazione:
                flash('Preparazione non trovata.', 'danger')
                return redirect(url_for('app_cucina.preparazioni'))

            tipiPreparazioni = service_t_tipipreparazioni.get_all_tipipreparazioni()
            alimenti = service_t_Alimenti.get_all()
            alimentiPerPrep = service_t_preparazionicontenuti.get_preparazioni_contenuti_by_id_preparazione(id_preparazione)
            associazione = service_t_AssociazionePiattiPreparazionie.get_id_piatto_by_preparazione(id_preparazione)

            tipi_quantita = service_t_tipoquantita.get_all_tipoquantita()
            preparazioni_base = service_t_preparazioni.get_all_preparazioni_base()  # Recupera le preparazioni di base
            
            # Riempie i form
            form = PreparazioniForm(obj=preparazione)
            alimform = AlimentoForm(obj=preparazione)

            form.fkTipoPreparazione.choices = [
                (tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni
            ]

            alimform.fkAlimento.choices = [
                (alimento['id'], alimento['alimento']) for alimento in alimenti
            ] + [
                (preparazione['id'] + 100000, preparazione['descrizione']) for preparazione in preparazioni_base
            ]

            alimform.fkTipoQuantita.choices = [
                (tipo_quantita['id'], tipo_quantita['tipo']) for tipo_quantita in tipi_quantita
            ]

            data = {
                'preparazione': {
                    'fkTipoPreparazione': preparazione.get('fkTipoPreparazione'),
                    'fkTipoPiatto': associazione.get('fkPiatto'),
                    'descrizione': preparazione.get('descrizione'),
                    'estivo': preparazione.get('estivo'),
                    'invernale': preparazione.get('invernale'),
                    'inizio': preparazione.get('inizio').strftime('%Y-%m-%d') if preparazione.get('inizio') else '',
                    'fine': preparazione.get('fine').strftime('%Y-%m-%d') if preparazione.get('fine') else '',
                    'immagine': preparazione.get('immagine')
                },
                'ingredienti': [],
                'scelte': {
                    'tipiPreparazioni': [(tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni],
                    'alimenti': [(alimento['id'], alimento['alimento']) for alimento in alimenti],
                    'tipiQuantita': [(tipo_quantita['id'], tipo_quantita['tipo']) for tipo_quantita in tipi_quantita]
                }
            }

            # Aggiungi ingredienti solo se presenti
            if alimentiPerPrep:
                data['ingredienti'] = [
                    {
                        'fkAlimento': ingrediente.get('fkAlimento'),
                        'quantita': ingrediente.get('quantita'),
                        'fkTipoQuantita': ingrediente.get('fkTipoQuantita'),
                        'note': ingrediente.get('note')
                    } for ingrediente in alimentiPerPrep if isinstance(ingrediente, dict)  # Assicurati che sia un dizionario
                ]
            
            return jsonify(data)

        if request.method == 'POST':
                
            # Recupera i dati dal form
            fkTipoPreparazione = request.form.get('fkTipoPreparazione')
            descrizione = request.form.get('descrizione')
            estivo = request.form.get('estivo') == '1'  # Converte in booleano
            invernale = request.form.get('invernale') == '1'  # Converte in booleano
            inizio = request.form.get('inizio') or None
            fine = request.form.get('fine') or None
            immagine = request.form.get('immagine')  # Gestisci l'immagine come necessario

            
            try:
                service_t_preparazioni.update(
                    id_preparazione,
                    fkTipoPreparazione=fkTipoPreparazione,
                    descrizione=descrizione,
                    isEstivo=estivo,
                    isInvernale=invernale,
                    inizio=inizio,
                    fine=fine,
                    immagine=immagine
                )
                
                # Gestisci gli ingredienti
                ingredient_list = json.loads(request.form.get('ingredientList', '[]'))  # Assicurati che sia una lista valida
                service_t_preparazionicontenuti.delete_preparazioni_contenuti(id_preparazione, utenteCancellazione=session.get('username'))  # Pulisci ingredienti esistenti

                for ingrediente in ingredient_list:
                    if isinstance(ingrediente, dict):
                        service_t_preparazionicontenuti.create_preparazioni_contenuti(
                            fkPreparazione=id_preparazione,
                            fkAlimento=int(ingrediente.get('fkAlimento')),
                            quantita=float(ingrediente.get('quantita', 0)),
                            fkTipoQuantita=int(ingrediente.get('fkTipoQuantita')),
                            note=ingrediente.get('note', '')
                        )
                
                flash('Preparazione modificata con successo!', 'success')
                return redirect(url_for('app_cucina.preparazioni'))  # Redirect alla lista delle preparazioni

            except Exception as e:
                flash(f'Errore durante la modifica della preparazione: {e}', 'danger')
                return redirect(url_for('app_cucina.preparazioni'))  # Redirect in caso di errore


        if request.method == 'DELETE':
            print(f"Request to delete preparazione with ID: {id_preparazione}")
            try:
                service_t_AssociazionePiattiPreparazionie.delete_associazione(fkPreparazione=id_preparazione, utenteCancellazione=session.get('username'))
                service_t_preparazionicontenuti.delete_preparazioni_contenuti(fkPreparazione=id_preparazione, utenteCancellazione=session.get('username'))
                service_t_preparazioni.delete_preparazione(id=id_preparazione, utenteCancellazione=session.get('username'))
                
                flash('Preparazione eliminata con successo!', 'success')
                return '', 204
            except Exception as e:
                print(f"Error deleting scheda: {e}")
                flash('Errore durante l\'eliminazione della preparazione.', 'danger')
                return '', 400

    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('preparazioni/get_tipi_piatti/<int:fkTipoPreparazione>', methods=['GET'])
def get_by_fkTipoPreparazione(fkTipoPreparazione):
    """
    Recupera i tipi di piatti associati a una specifica tipologia di preparazione.

    Questa funzione consente di:
    - Ottenere la lista dei piatti disponibili per un determinato tipo di preparazione.
    - Se non ci sono piatti associati, restituisce l'elenco completo di tutti i piatti.
    """
    id_modificato= service_t_AssociazioneTipiPiattiTipiPreparazioni.get_fkTipoPatto_by_fkTipoPeparazione(fkTipoPreparazione)
    piatti = service_t_Piatti.get_by_fkTipoPiatto(id_modificato)
    print(piatti)
    tutti_i_piatti = service_t_Piatti.get_all()
    return jsonify(piatti if piatti else tutti_i_piatti)



@app_cucina.route('/piatti', methods=['GET', 'POST'])
def piatti():
    """
    Gestisce la visualizzazione e la creazione di piatti.

    Questa funzione consente di:
    - Visualizzare l'elenco di tutti i piatti esistenti.
    - Creare un nuovo piatto attraverso un form.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e mostra tutti i piatti disponibili insieme alle rispettive tipologie.
    - **POST**: Consente di creare un nuovo piatto utilizzando i dati inviati attraverso un form.

    Args:
        Nessuno. Le informazioni sugli utenti e i piatti sono gestite a livello di sessione e servizio.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'piatti.html' con i seguenti dati:
                    - Elenco di tutti i piatti.
                    - Mappa delle tipologie di piatti con i rispettivi ID e descrizioni.
                    - Form per la creazione di un nuovo piatto.
            - **POST**:
                - Se il form è valido e i dati sono corretti:
                    - Viene creato un nuovo piatto nel database.
                    - Reindirizza alla pagina dei piatti per mostrare l'elenco aggiornato.
                - Se c'è un errore durante la creazione:
                    - Restituisce un messaggio di errore con status code 500.
                    - Mantiene il form con gli errori di validazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Il form di creazione di un piatto include campi per selezionare la tipologia, il codice, il titolo, la descrizione,
          lo stato di 'inMenu', l'ordinatore, e registra l'utente che ha inserito il piatto.
    """
    # Verificare se l'utente è autenticato
    if 'authenticated' in session:
        # Ottenere tutti i piatti e le tipologie di piatti dal servizio
        piatti = service_t_Piatti.get_all()
        tipologia_piatti = service_t_TipiPiatti.get_all()

        # Mappare le tipologie di piatti per l'uso nel template
        TipoPiatto_map = {int(tipoPiatto['id']): tipoPiatto['descrizione'] for tipoPiatto in tipologia_piatti}

        # Creare un'istanza del form per l'aggiunta di piatti
        form = PiattiForm()

        # Popolare le scelte per il campo fkTipoPiatto nel form
        form.fkTipoPiatto.choices = [(tipoPiatto['id'], tipoPiatto['descrizione']) for tipoPiatto in tipologia_piatti]
    
        # Se il form è stato inviato e è valido, processa i dati del form
        if form.validate_on_submit():         
           
            try:
                service_t_Piatti.create(
                    fkTipoPiatto=form.fkTipoPiatto.data, 
                    codice=form.codice.data, 
                    titolo=form.titolo.data,
                    descrizione=form.descrizione.data, 
                    inMenu=form.inMenu.data, 
                    ordinatore=form.ordinatore.data, 
                    utenteInserimento=session.get('username')
                )
                app.logger.debug("Piatto creato con successo nel database.")
            except Exception as e:
                app.logger.error(f"Errore durante la creazione del piatto: {str(e)}")
                return {'Error': str(e)}, 500

            # Se il salvataggio nel database ha successo, aggiorna la lista dei piatti
            piatti = service_t_Piatti.get_all()

            return redirect(url_for('app_cucina.piatti'))
    
    # Se il form non è stato inviato o non è valido, mostra il template con il form vuoto o con errori
        return render_template(
            'piatti.html',
            piatti=piatti,
            tipologia_piatti=tipologia_piatti,
            TipoPiatto_map=TipoPiatto_map,
            form=form
            )
    
    # Se l'utente non è autenticato, reindirizzalo alla pagina di login
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/piatti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_piatti(id):
    """
    Gestisce le operazioni di recupero, aggiornamento e cancellazione di un piatto.

    Questa funzione consente di:
    - Recuperare i dettagli di un piatto esistente tramite l'ID specificato.
    - Aggiornare le informazioni di un piatto esistente.
    - Cancellare un piatto esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli del piatto con l'ID specificato in formato JSON.
    - **PUT**: Aggiorna i dettagli del piatto con l'ID specificato utilizzando i dati forniti nel modulo.
    - **DELETE**: Cancellare il piatto con l'ID specificato.

    Args:
        id (int): L'ID del piatto da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli del piatto, se trovato.
                - Status code 404 se il piatto non è trovato.
            - **PUT**:
                - JSON con un messaggio di successo o errore a seconda del risultato dell'operazione di aggiornamento.
                - Status code 400 se ci sono errori di validazione del form.
                - Status code 500 in caso di errore durante l'aggiornamento.
            - **DELETE**:
                - Status code 204 se il piatto è stato eliminato con successo.
                - Status code 400 in caso di errore durante l'eliminazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """
    if 'authenticated' in session:


        if request.method == 'GET':
            piatto = service_t_Piatti.get_by_id(id)
            
            # Ensure tipologia_piatti is correctly retrieved
            tipologia_piatti = service_t_TipiPiatti.get_all()  # Or however you retrieve it
            
            # Create the form with existing piatto data
            form = PiattiForm(obj=piatto)
            form.fkTipoPiatto.choices = [(tipoPiatto['id'], tipoPiatto['descrizione']) for tipoPiatto in tipologia_piatti]
            
            if piatto:
                return jsonify({
                    'fkTipoPiatto': piatto.get('fkTipoPiatto'),  # Corretto per restituire il valore del piatto
                    'codice': piatto.get('codice'),
                    'titolo': piatto.get('titolo'),
                    'descrizione': piatto.get('descrizione'),
                    'inMenu': piatto.get('inMenu'),
                    'ordinatore': piatto.get('ordinatore')
                    })
            else:
                flash('Piatto non trovato.', 'danger')
                return '', 404  # Status code 404 Not Found


        if request.method == 'PUT':
            tipologia_piatti = service_t_TipiPiatti.get_all()  # Recupera le opzioni
            form = PiattiForm(request.form)
            form.fkTipoPiatto.choices = [(tipoPiatto['id'], tipoPiatto['descrizione']) for tipoPiatto in tipologia_piatti]
            
            if form.validate_on_submit():
                try:
                    service_t_Piatti.update(
                        id=id,
                        fkTipoPiatto=form.fkTipoPiatto.data,
                        codice=form.codice.data,
                        titolo=form.titolo.data,
                        descrizione=form.descrizione.data,
                        inMenu=form.inMenu.data,
                        ordinatore=form.ordinatore.data,
                        utenteInserimento=session.get('username')
                    )


                    # Restituisci una risposta JSON senza redirect
                    return jsonify({'message': 'Piatto aggiornato con successo!'}), 200

                except Exception as e:
                    print(f"Errore durante l'aggiornamento: {e}")
                    return jsonify({'error': 'Errore durante l\'aggiornamento del piatto'}), 500

            else:
                # Gestisci errori di validazione del form
                return jsonify({'error': 'Errore nella validazione del form'}), 400


        if request.method == 'DELETE':
            try:
                service_t_Piatti.delete(id, utenteCancellazione=session.get('username'))
                flash('Piatto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content
            
            except Exception as e:
                print(f"Error deleting dish: {e}")
                flash('Errore durante l\'eliminazione del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request

    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/tipologia_piatti', methods=['GET', 'POST'])
def tipologia_piatti():
    """
    Gestisce la visualizzazione e la creazione delle tipologie di piatti.

    Questa funzione consente di:
    - Visualizzare l'elenco delle tipologie di piatti esistenti.
    - Creare una nuova tipologia di piatto se l'utente è autenticato.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutte le tipologie di piatti esistenti e un modulo per la creazione di una nuova tipologia.
    - **POST**: Crea una nuova tipologia di piatto con i dati forniti nel modulo, se l'utente ha effettuato il login.

    Args:
        Nessuno. La funzione gestisce l'autenticazione tramite sessione per garantire l'accesso.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'tipologia_piatti.html' con i seguenti dati:
                    - Elenco delle tipologie di piatti esistenti.
                    - Un modulo per inserire una nuova tipologia di piatto.
            - **POST**:
                - Se la creazione della tipologia di piatto ha successo, reindirizza alla stessa pagina con un messaggio di conferma.
                - Se il modulo non è valido, rimane sulla stessa pagina mostrando eventuali messaggi di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza il servizio `service_t_TipiPiatti` per recuperare e gestire le tipologie di piatti.
        - La funzione gestisce la validazione del modulo e la comunicazione di successi o errori all'utente.
    """
    
    if 'authenticated' in session:
        tipologia_piatti = service_t_TipiPiatti.get_all()

        form = TipologiaPiattiForm()

        if form.validate_on_submit():
            
            service_t_TipiPiatti.create(
                descrizione=form.descrizione.data, 
                descrizionePlurale=form.descrizionePlurale.data, 
                inMenu=form.inMenu.data, 
                ordinatore=form.ordinatore.data, 
                color=form.color.data, 
                backgroundColor=form.backgroundColor.data, 
                utenteInserimento=session.get('username'))
            
            flash('Scheda aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.tipologia_piatti'))
            
    
        return render_template('tipologia_piatti.html',
                               tipologia_piatti=tipologia_piatti,
                               form=form)
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/tipologia_piatti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_tipologia_piatti(id):
    """
    Gestisce le operazioni di recupero, aggiornamento e cancellazione di una tipologia di piatto.

    Questa funzione consente di:
    - Recuperare i dettagli di una tipologia di piatto esistente tramite l'ID specificato.
    - Aggiornare le informazioni di una tipologia di piatto esistente.
    - Cancellare una tipologia di piatto esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli della tipologia di piatto con l'ID specificato in formato JSON.
    - **PUT**: Aggiorna i dettagli della tipologia di piatto con l'ID specificato utilizzando i dati forniti nel modulo.
    - **DELETE**: Cancellare la tipologia di piatto con l'ID specificato.

    Args:
        id (int): L'ID della tipologia di piatto da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli della tipologia di piatto, se trovata.
                - Status code 404 se la tipologia di piatto non è trovata.
            - **PUT**:
                - JSON con un messaggio di successo o errore a seconda del risultato dell'operazione di aggiornamento.
                - Status code 400 se ci sono errori di validazione del form.
                - Status code 500 in caso di errore durante l'aggiornamento.
            - **DELETE**:
                - Status code 204 se la tipologia di piatto è stata eliminata con successo.
                - Status code 400 in caso di errore durante l'eliminazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """
    if 'authenticated' in session:


        if request.method == 'GET':
            
            # Ensure tipologia_piatti is correctly retrieved
            tipologia_piatti = service_t_TipiPiatti.get_by_id(id)  # Or however you retrieve it
            
            # Create the form with existing piatto data
            form = TipologiaPiattiForm(obj=tipologia_piatti)
            
            if tipologia_piatti:
                return jsonify({
                    'descrizione': tipologia_piatti.get('descrizione'),  
                    'descrizionePlurale': tipologia_piatti.get('descrizionePlurale'),
                    'inMenu': tipologia_piatti.get('inMenu'),
                    'ordinatore': tipologia_piatti.get('ordinatore'),
                    'color': tipologia_piatti.get('color'),
                    'backgroundColor': tipologia_piatti.get('backgroundColor')
                    })
            else:
                flash('Tipologia di piatto non trovato.', 'danger')
                return '', 404  # Status code 404 Not Found


        if request.method == 'PUT':
            tipologia_piatti = service_t_TipiPiatti.get_all()  # Recupera le opzioni
            form = TipologiaPiattiForm(request.form)
            
            if form.validate_on_submit():
                try:
                    service_t_TipiPiatti.update(
                        id=id,
                        descrizione=form.descrizione.data, 
                        descrizionePlurale=form.descrizionePlurale.data, 
                        inMenu=form.inMenu.data, 
                        ordinatore=form.ordinatore.data, 
                        color=form.color.data, 
                        backgroundColor=form.backgroundColor.data, 
                        utenteInserimento=session.get('username'))

                    
                    # Restituisci una risposta JSON senza redirect
                    return jsonify({'message': 'Tipologia piatto aggiornato con successo!'}), 200

                except Exception as e:
                    print(f"Errore durante l'aggiornamento: {e}")
                    return jsonify({'error': 'Errore durante l\'aggiornamento della tipologia del piatto'}), 500

            else:
                # Gestisci errori di validazione del form
                return jsonify({'error': 'Errore nella validazione del form'}), 400



        if request.method == 'DELETE':
            try:
                service_t_TipiPiatti.delete(id, utenteCancellazione=session.get('username'))
                flash('Tipolgia piatto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content
            
            except Exception as e:
                print(f"Error deleting dish: {e}")
                flash('Errore durante l\'eliminazione della tipologia del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request

    else:
        return redirect(url_for('app_cucina.login'))  



@app_cucina.route('/reparti', methods=['GET', 'POST'])
def reparti():
    """
    Gestisce la visualizzazione e la creazione dei reparti.

    Questa funzione consente di:
    - Visualizzare l'elenco dei reparti esistenti.
    - Creare un nuovo reparto se l'utente è autenticato.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutti i reparti esistenti e un modulo per la creazione di un nuovo reparto.
    - **POST**: Crea un nuovo reparto con i dati forniti nel modulo, se l'utente ha effettuato il login.

    Args:
        Nessuno. La funzione gestisce l'autenticazione tramite sessione per garantire l'accesso.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'reparti.html' con i seguenti dati:
                    - Elenco dei reparti esistenti.
                    - Un modulo per inserire un nuovo reparto.
            - **POST**:
                - Se la creazione del reparto ha successo, reindirizza alla stessa pagina con un messaggio di conferma.
                - Se il modulo non è valido, rimane sulla stessa pagina mostrando eventuali messaggi di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza il servizio `service_t_Reparti` per recuperare e gestire i reparti.
        - La funzione gestisce la validazione del modulo e la comunicazione di successi o errori all'utente.
    """

    
    if 'authenticated' in session:
        reparti = service_t_Reparti.get_all()
        form = RepartiForm()

        if form.validate_on_submit():

            service_t_Reparti.create(
                codiceAreas=form.codiceAreas.data, 
                descrizione=form.descrizione.data, 
                sezione=form.sezione.data, 
                ordinatore=form.ordinatore.data,
                padiglione=form.padiglione.data, 
                piano=form.piano.data, 
                lato=form.lato.data, 
                inizio=form.inizio.data,
                fine=form.fine.data,
                utenteInserimento=session.get('username')
                            )
            
            flash('reparto aggiunto con successo!', 'success')
            return redirect(url_for('app_cucina.reparti'))
    

        return render_template('reparti.html',
                               reparti=reparti,
                               form=form)
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/reparti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_reparti(id):
    """
    Gestisce le operazioni di recupero, aggiornamento e cancellazione di un reparto.

    Questa funzione consente di:
    - Recuperare i dettagli di un reparto esistente tramite l'ID specificato.
    - Aggiornare le informazioni di un reparto esistente.
    - Cancellare un reparto esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli del reparto con l'ID specificato in formato JSON.
    - **PUT**: Aggiorna i dettagli del reparto con l'ID specificato utilizzando i dati forniti nel modulo.
    - **DELETE**: Cancellare il reparto con l'ID specificato.

    Args:
        id (int): L'ID del reparto da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli del reparto, se trovato.
                - Status code 404 se il reparto non è trovato.
            - **PUT**:
                - JSON con un messaggio di successo o errore a seconda del risultato dell'operazione di aggiornamento.
                - Status code 400 se ci sono errori di validazione del form.
                - Status code 500 in caso di errore durante l'aggiornamento.
            - **DELETE**:
                - Status code 204 se il reparto è stato eliminato con successo.
                - Status code 400 in caso di errore durante l'eliminazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """
    if 'authenticated' in session:

        if request.method == 'GET':
                 
            reparto = service_t_Reparti.get_by_id(id)  
            
            # Create the form with existing Reparto data
            form = RepartiForm(obj=reparto)
            
            if reparto:
                return jsonify({
                    'codiceAreas': reparto.get('codiceAreas'),
                    'descrizione': reparto.get('descrizione'),   
                    'sezione': reparto.get('sezione'),
                    'ordinatore': reparto.get('ordinatore'),
                    'padiglione': reparto.get('padiglione'),
                    'piano': reparto.get('piano'),
                    'lato': reparto.get('lato'),
                    'inizio': reparto.get('inizio'), 
                    'fine': reparto.get('fine')

                    })
            else:
                flash('Reparto non trovato.', 'danger')
                return '', 404  # Status code 404 Not Found


        if request.method == 'PUT':
            reparto = service_t_Reparti.get_all()  # Recupera le opzioni
            form = RepartiForm(request.form)
            
            if form.validate_on_submit():
                try:
                    service_t_Reparti.update(
                        id=id,
                        codiceAreas=form.codiceAreas.data, 
                        descrizione=form.descrizione.data, 
                        sezione=form.sezione.data, 
                        ordinatore=form.ordinatore.data,
                        padiglione=form.padiglione.data, 
                        piano=form.piano.data, 
                        lato=form.lato.data, 
                        inizio=form.inizio.data,
                        fine=form.fine.data,
                        utenteInserimento=session.get('username')
                    )

                    
                    # Restituisci una risposta JSON senza redirect
                    return jsonify({'message': 'Reparto aggiornato con successo!'}), 200

                except Exception as e:
                    print(f"Errore durante l'aggiornamento: {e}")
                    return jsonify({'error': 'Errore durante l\'aggiornamento del reparto'}), 500

            else:
                # Gestisci errori di validazione del form
                return jsonify({'error': 'Errore nella validazione del form'}), 400



        if request.method == 'DELETE':
            try:
                service_t_Reparti.delete(id, utenteCancellazione=session.get('username'))
                flash('Reparto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content
            
            except Exception as e:
                print(f"Error deleting dish: {e}")
                flash('Errore durante l\'eliminazione della Reparto.', 'danger')
                return '', 400  # Status code 400 Bad Request

    else:
        return redirect(url_for('app_cucina.login'))  


@app_cucina.route('/servizi', methods=['GET', 'POST'])
def servizi():
    """
    Gestisce la visualizzazione e la creazione dei servizi.

    Questa funzione consente di:
    - Visualizzare l'elenco dei servizi esistenti.
    - Creare un nuovo servizio se l'utente è autenticato.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutti i servizi esistenti e un modulo per la creazione di un nuovo servizio.
    - **POST**: Crea un nuovo servizio con i dati forniti nel modulo, se l'utente ha effettuato il login.

    Args:
        Nessuno. La funzione gestisce l'autenticazione tramite sessione per garantire l'accesso.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'servizi.html' con i seguenti dati:
                    - Elenco dei servizi esistenti.
                    - Un modulo per inserire un nuovo servizio.
            - **POST**:
                - Se la creazione del servizio ha successo, ricarica la pagina mostrando l'elenco aggiornato dei servizi.
                - Se il modulo non è valido, rimane sulla stessa pagina mostrando eventuali messaggi di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza il servizio `service_t_Servizi` per recuperare e gestire i servizi.
        - La funzione gestisce la validazione del modulo e la comunicazione di successi o errori all'utente.
    """
    if 'authenticated' in session:
        servizi = service_t_Servizi.get_all_servizi()

        form = ServiziForm() 

        if form.validate_on_submit():
            service_t_Servizi.create_servizio(
                descrizione=form.descrizione.data,
                ordinatore=form.ordinatore.data,
                inMenu=form.inMenu.data
            )

        return render_template('servizi.html',servizi=servizi, form=form)
    else:
        return redirect(url_for('app_cucina.login'))
    


@app_cucina.route('/servizi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_servizi(id):
    """
    Gestisce le operazioni di recupero, aggiornamento e cancellazione di un servizio.

    Questa funzione consente di:
    - Recuperare i dettagli di un servizio esistente tramite l'ID specificato.
    - Aggiornare le informazioni di un servizio esistente.
    - Cancellare un servizio esistente (attualmente la cancellazione è commentata).

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli del servizio con l'ID specificato in formato JSON.
    - **PUT**: Aggiorna i dettagli del servizio con l'ID specificato utilizzando i dati forniti nel modulo.
    - **DELETE**: (non attualmente implementata) Cancellare il servizio con l'ID specificato.

    Args:
        id (int): L'ID del servizio da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli del servizio, se trovato.
                - Status code 404 se il servizio non è trovato.
            - **PUT**:
                - JSON con un messaggio di successo o errore a seconda del risultato dell'operazione di aggiornamento.
                - Status code 400 se ci sono errori di validazione del form.
                - Status code 500 in caso di errore durante l'aggiornamento.
            - **DELETE**:
                - Attualmente non implementata, la cancellazione restituirebbe un messaggio di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """
    if 'authenticated' in session:


        if request.method == 'GET':
            
            
            servizio = service_t_Servizi.get_servizio_by_id(id)  
            
            # Create the form with existing Reparto data
            form = ServiziForm(obj=servizio)
            
            if servizio:
                return jsonify({
                    
                    'descrizione': servizio.get('descrizione'),                     
                    'ordinatore': servizio.get('ordinatore'),
                    'inMenu': servizio.get('inMenu')

                    })
            else:
                flash('Servizio non trovato.', 'danger')
                return '', 404  # Status code 404 Not Found


        if request.method == 'PUT':
            servizio = service_t_Servizi.get_all_servizi()  # Recupera le opzioni
            form = ServiziForm(request.form)
            
            if form.validate_on_submit():
                try:
                    service_t_Servizi.update_servizio(
                        id=id,                                     
                        descrizione=form.descrizione.data, 
                        ordinatore=form.ordinatore.data,
                        inMenu=form.inMenu.data
                                       
                    )

                    
                    # Restituisci una risposta JSON senza redirect
                    return jsonify({'message': 'Servizio aggiornato con successo!'}), 200

                except Exception as e:
                    print(f"Errore durante l'aggiornamento: {e}")
                    return jsonify({'error': 'Errore durante l\'aggiornamento del Servizio'}), 500

            else:
                # Gestisci errori di validazione del form
                return jsonify({'error': 'Errore nella validazione del form'}), 400


        # scrivo la delete nel caso servisse ma ho commentato 
        if request.method == 'DELETE':
            try:
                
                # service_t_Servizi.delete_servizio(id)
                flash('impossibile eliminare il servizio!', 'success')
                return '', 204  # Status code 204 No Content
            
            except Exception as e:
                print(f"Error deleting dish: {e}")
                flash('Errore durante l\'eliminazione del servizio.', 'danger')
                return '', 400  # Status code 400 Bad Request

    else:
        return redirect(url_for('app_cucina.login'))  



@app_cucina.route('/tipologia_menu', methods=['GET', 'POST'])
def tipologia_menu():
    """
    Gestisce la visualizzazione e la creazione delle tipologie di menu.

    Questa funzione consente di:
    - Visualizzare l'elenco delle tipologie di menu esistenti.
    - Creare una nuova tipologia di menu se l'utente è autenticato.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutte le tipologie di menu esistenti e un modulo per la creazione di una nuova tipologia di menu.
    - **POST**: Crea una nuova tipologia di menu con i dati forniti nel modulo, se l'utente ha effettuato il login.

    Args:
        Nessuno. La funzione gestisce l'autenticazione tramite sessione per garantire l'accesso.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'tipologia_menu.html' con i seguenti dati:
                    - Elenco delle tipologie di menu esistenti.
                    - Un modulo per inserire una nuova tipologia di menu.
            - **POST**:
                - Se la creazione della tipologia di menu ha successo, ricarica la pagina mostrando l'elenco aggiornato delle tipologie di menu.
                - Se il modulo non è valido, rimane sulla stessa pagina mostrando eventuali messaggi di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza il servizio `service_t_TipiMenu` per recuperare e gestire le tipologie di menu.
        - La funzione gestisce la validazione del modulo e mostra un messaggio di successo quando una nuova tipologia di menu viene aggiunta correttamente.
    """
    if 'authenticated' in session:
        tipologie_menu = service_t_TipiMenu.get_all()
    
        form = TipologiaMenuForm()

        if form.validate_on_submit():
            
            service_t_TipiMenu.create(
                descrizione=form.descrizione.data, 
                ordinatore=form.ordinatore.data, 
                color=form.color.data, 
                backgroundColor=form.backgroundColor.data, 
                utenteInserimento=session.get('username'))
            
            flash('tipo menu aggiunto con successo!', 'success')
            return redirect(url_for('app_cucina.tipologia_menu'))


        return render_template('tipologia_menu.html', 
                               tipologie_menu=tipologie_menu, 
                               form=form)
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/tipologia_menu/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def nodifica_tipologia_menu(id):
    """
    Gestisce le operazioni di recupero, aggiornamento e cancellazione di una tipologia di menu.

    Questa funzione consente di:
    - Recuperare i dettagli di una tipologia di menu esistente tramite l'ID specificato.
    - Aggiornare le informazioni di una tipologia di menu esistente.
    - Cancellare una tipologia di menu esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli della tipologia di menu con l'ID specificato in formato JSON.
    - **PUT**: Aggiorna i dettagli della tipologia di menu con l'ID specificato utilizzando i dati forniti nel modulo.
    - **DELETE**: Cancella la tipologia di menu con l'ID specificato.

    Args:
        id (int): L'ID della tipologia di menu da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli della tipologia di menu, se trovata.
                - Status code 404 se la tipologia di menu non è trovata.
            - **PUT**:
                - JSON con un messaggio di successo o errore a seconda del risultato dell'operazione di aggiornamento.
                - Status code 400 se ci sono errori di validazione del form.
                - Status code 500 in caso di errore durante l'aggiornamento.
            - **DELETE**:
                - JSON con un messaggio di successo o errore a seconda del risultato della cancellazione.
                - Status code 200 se la cancellazione è avvenuta con successo.
                - Status code 400 in caso di errore durante la cancellazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """
    if 'authenticated' in session:


        if request.method == 'GET':
            
            # Ensure tipologia_menu is correctly retrieved
            tipologia_menu = service_t_TipiMenu.get_by_id(id)  # Or however you retrieve it
            
            # Create the form with existing menu data
            form = TipologiaMenuForm(obj=tipologia_menu)
            
            if tipologia_menu:
                return jsonify({
                    'descrizione': tipologia_menu.get('descrizione'),  # Corretto per restituire il valore del menu
                    'ordinatore': tipologia_menu.get('ordinatore'),
                    'color': tipologia_menu.get('color'),
                    'backgroundColor': tipologia_menu.get('backgroundColor')
                    })
            else:
                flash('Tipologia di Menu non trovato.', 'danger')
                return '', 404  # Status code 404 Not Found


        if request.method == 'PUT':
            tipologia_menu = service_t_TipiMenu.get_all()  # Recupera le opzioni
            form = TipologiaMenuForm(request.form)
            
            if form.validate_on_submit():
                try:
                    service_t_TipiMenu.update(
                        id=id,
                        descrizione=form.descrizione.data, 
                        ordinatore=form.ordinatore.data, 
                        color=form.color.data, 
                        backgroundColor=form.backgroundColor.data, 
                        utenteInserimento=session.get('username'))

                    # Restituisci una risposta JSON senza redirect
                    return jsonify({'message': 'Tipologia menu aggiornato con successo!'}), 200

                except Exception as e:
                    print(f"Errore durante l'aggiornamento: {e}")
                    return jsonify({'error': 'Errore durante l\'aggiornamento dela tipologia del menu'}), 500

            else:
                # Gestisci errori di validazione del form
                return jsonify({'error': 'Errore nella validazione del form'}), 400



        if request.method == 'DELETE':
            try:
                service_t_TipiMenu.delete(id, utenteCancellazione=session.get('username'))
                flash('Tipologia Menu eliminato con successo!', 'success')
                return jsonify({'message': f'Menu {id} eliminato con successo.'}), 200  # Cambiato a 200 se vuoi includere un messaggio
            except Exception as e:
                print(f"Error deleting menu: {e}")  # Potresti voler usare un logging più sofisticato
                flash('Errore durante l\'eliminazione della tipologia del menu.', 'danger')
                return jsonify({'message': f'Errore nell\'eliminazione del menu {id}: {str(e)}'}), 400
        else:
            return redirect(url_for('app_cucina.login'))  



@app_cucina.route('/menu', methods=['GET', 'POST'])
def menu():
    """
    Gestisce la visualizzazione e la clonazione del menu per un mese specifico.

    Questa funzione consente di:
    - Visualizzare il menu esistente per un determinato mese e tipo di menu.
    - Clonare il menu esistente per un nuovo mese.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza i menu esistenti per il mese e il tipo di menu specificati.
    - **POST**: Clona un menu esistente per il giorno specificato o per un insieme di giorni consecutivi.

    Args:
        Nessuno. Le informazioni sul mese, il tipo di menu e i menu esistenti sono gestite attraverso le query string e i dati di sessione.

    Query Parameters:
        year (int, optional): L'anno da visualizzare o su cui clonare il menu (default è l'anno corrente).
        month (int, optional): Il mese da visualizzare o su cui clonare il menu (default è il mese corrente).
        tipo_menu (int, optional): Il tipo di menu da visualizzare o su cui clonare il menu (default è '1').

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'menu.html' con i seguenti dati:
                    - Informazioni sui menu esistenti per la data e il tipo di menu selezionati.
                    - Mappa delle tipologie di menu e delle preparazioni associate.
                    - Form per clonare un menu esistente.
                    - Dati aggregati sui menu, come le associazioni tra piatti e preparazioni.

            - **POST**:
                - Se il form di clonazione è valido, il menu viene clonato per il giorno e i servizi selezionati.
                - Reindirizza alla pagina aggiornata del menu.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come tipologie di menu, piatti e servizi associati.
        - Il form per la clonazione del menu consente di selezionare un menu esistente e specificare una data per il clone.
        - Se si verifica un errore durante la clonazione, viene visualizzato un messaggio di errore appropriato.
    """


    if 'authenticated' in session:
        #fa visualizare i mesi in italiano
        locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
        # Ottieni i parametri dai query string
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        tipo_menu = request.args.get('tipo_menu', '1')

        # Crea un oggetto Calendar
        cal = calendar.Calendar(firstweekday=0)  # 0 per lunedì, 6 per domenica

        # Ottieni la prima e l'ultima data del mese
        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])

        # Ottieni la settimana che contiene il primo giorno del mese
        first_week_start = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        last_week_end = last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday()))

        # Crea un intervallo di giorni che include la settimana precedente e quella successiva
        days = [first_week_start + timedelta(days=i) for i in range((last_week_end - first_week_start).days + 1)]

        # Raggruppa i giorni in settimane
        full_weeks = [days[i:i + 7] for i in range(0, len(days), 7)]

        # Mappa per i giorni della settimana
        weekdays = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']  

        # Calcola il numero della settimana per ogni giorno
        week_numbers = {}
        previous_iso_week_number = None

        for week_index, week in enumerate(full_weeks):
            for day in week:
                if day:
                    # Calcola l'anno e il mese corrente
                    actual_year = day.year
                    actual_month = day.month

                    # Ottieni il numero di settimana ISO
                    iso_week_number = day.isocalendar()[1]

                    # Se è la prima iterazione o se è cambiata la settimana ISO, calcola la settimana ciclica
                    if previous_iso_week_number is None or iso_week_number != previous_iso_week_number:
                        cycle_week_number = (iso_week_number - 1) % 4 + 1
                        previous_iso_week_number = iso_week_number

                    # Memorizza il numero di settimana ciclica
                    week_numbers[(actual_year, actual_month, day.day)] = cycle_week_number

        # Recupera i dati dal servizio
        tipologie_menu = service_t_TipiMenu.get_all()
        menu = service_t_Menu.get_by_date_range(first_week_start, last_week_end, tipo_menu)
        associazione = service_t_AssociazionePiattiPreparazionie.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()
        
        servizi = service_t_Servizi.get_all_servizi()      
        piatti = service_t_Piatti.get_all()   
        tipologie_piatti = service_t_TipiPiatti.get_all()
        tipologia_piatti_map = {int(piatto['id']): piatto['descrizionePlurale'] for piatto in tipologie_piatti}

        
        # Recupera gli ID dei menu filtrati per il mese corrente
        menu_ids = [m.get('id') for m in menu if m.get('id') is not None]

        # Recupera tutti i servizi associati ai menu per il mese
        menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(menu_ids)
        
        # Crea una mappa per gli ID dei servizi associati ai menu
        menu_servizi_map = {}
        for ms in menu_servizi:
            if ms['fkMenu'] not in menu_servizi_map:
                menu_servizi_map[ms['fkMenu']] = {}
            menu_servizi_map[ms['fkMenu']][ms['fkServizio']] = ms['id']
        
        # Organizza i dati per giorno e servizio
        menu_per_giorno = {}
        for menu_item in menu:
            date_key = datetime.strptime(menu_item['data'], '%Y-%m-%d').strftime('%Y-%m-%d')
            if date_key not in menu_per_giorno:
                menu_per_giorno[date_key] = {'id_menu': menu_item['id']}
            # Aggiungi servizi per pranzo e cena
            for servizio in servizi:
                servizio_id = menu_servizi_map.get(menu_item['id'], {}).get(servizio['id'])
                menu_per_giorno[date_key][servizio['descrizione']] = servizio_id

        # Recupera i piatti per ogni servizio dinamicamente
        piattimenu = {}
        for servizio_id in set(id for ids in menu_servizi_map.values() for id in ids.values()):
            piattimenu[servizio_id] = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(servizio_id)

        # Crea una mappa dei piatti e delle preparazioni
        piatti_map = {int(piatto['id']): piatto['fkTipoPiatto'] for piatto in piatti}
        codice_map = {int(piatto['id']): piatto['codice'] for piatto in piatti}

        preparazioni_map = {int(preparazione['id']): preparazione['descrizione'] for preparazione in preparazioni}

        # Mappa per associare i piatti e le preparazioni
        associazione_map = {}
        for tipo_associa in associazione:
            piatto_nome = piatti_map.get(tipo_associa['fkPiatto'], 'Sconosciuto')
            piatto_codice = codice_map.get(tipo_associa['fkPiatto'], 'Sconosciuto')
            preparazione_descrizione = preparazioni_map.get(tipo_associa['fkPreparazione'], 'Sconosciuto')
            associazione_map[tipo_associa['id']] = {
                'piatto': piatto_nome,
                'codice': piatto_codice,
                'preparazione': preparazione_descrizione
            }

        clona_mese = CloneMenuForm() 
        form = CloneMenuForm()

        if request.method == 'POST':
            if clona_mese.validate_on_submit():
                try:
                    # Recupera la data di clonazione e il numero di giorni
                    clone_date_str = form.clone_date.data.strftime('%Y-%m-%d')
                    clone_date = datetime.strptime(clone_date_str, '%Y-%m-%d')
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))
                    utente_inserimento = session.get('username')

                    # Recupera gli ID dei menu dal form
                    menu_ids = request.form.get('menu_ids').split(',')

                    # Recupera i servizi associati ai menu
                    menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(menu_ids)

                    for index, menu_id_str in enumerate(menu_ids):
                        menu_id = int(menu_id_str)  # Converti menu_id in intero
                        giorno_clonazione = clone_date + timedelta(days=index)
                        

                        # Trova i servizi associati a questo menu
                        servizi_per_menu = [servizio for servizio in menu_servizi if servizio['fkMenu'] == menu_id]
                        
                        if not servizi_per_menu:
                            print(f"Nessun servizio trovato per il menu ID {menu_id}")

                        for servizio in servizi_per_menu:
                            clona_menu(servizio['id'], giorno_clonazione.strftime('%Y-%m-%d'), utente_inserimento)

                    flash('Mese clonato con successo!', 'success')
                    return redirect(next_url)

                except Exception as e:
                    print(f"Errore: {str(e)}") 
            
            if form.validate_on_submit():
                try:
                    menu_id = request.form['menu_id']
                    clone_date = form.clone_date.data.strftime('%Y-%m-%d')
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))
                    utente_inserimento = session.get('username')

                    # Chiama la funzione per clonare il menu
                    if clona_menu(menu_id, clone_date, utente_inserimento):
                        flash('Menu clonato con successo!', 'success')
                        return redirect(next_url)
                    else:
                        return redirect(url_for('app_cucina.menu'))

                except Exception as e:
                    flash(f"Errore durante la clonazione del menu: {str(e)}", 'error')
                    print(f"Errore durante la clonazione del menu: {str(e)}")


        return render_template(
            'menu.html',
            year=year,
            month=month,
            month_name=calendar.month_name[month],
            full_weeks=full_weeks,
            weekdays=weekdays,
            tipologie_menu=tipologie_menu,
            menu_per_giorno=menu_per_giorno,
            piatti_map=piatti_map,
            preparazioni_map=preparazioni_map,
            associazione_map=associazione_map,
            piattimenu=piattimenu,  # Passa piattimenu al template
            preparazioni=preparazioni,
            datetime=datetime,
            calendar=calendar,
            week_numbers=week_numbers,  # Passa i numeri delle settimane al template
            form=form,
            clona_mese=clona_mese,
            menu_ids=menu_ids,
            servizi=servizi,
            piatti=piatti,
            tipologia_piatti_map=tipologia_piatti_map
                    
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/menu/<int:id_menu>', methods=['DELETE'])
def cose_menu(id_menu):
    """
    Gestisce l'eliminazione di un menu specifico.

    Questa funzione consente di:
    - Eliminare un menu associato all'identificativo fornito.
    
    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **DELETE**: Rimuove il menu specificato dall'ID fornito.

    Args:
        id_menu (int): L'ID del menu da eliminare.

    Returns:
        Response:
            - **DELETE**:
                - Se l'eliminazione è avvenuta con successo, restituisce un codice di stato 204 (No Content).
                - Se si verifica un errore durante l'eliminazione, restituisce un codice di stato 400 (Bad Request).
                - Se l'utente non è autenticato, viene reindirizzato alla pagina di login con un messaggio di avviso.

    Notes:
        - Se l'utente non è autenticato, viene visualizzato un messaggio di avviso per effettuare il login.
        - La funzione utilizza il servizio `service_t_MenuServiziAssociazione` per recuperare e eliminare il menu.
        - Se l'eliminazione ha successo, viene visualizzato un messaggio di conferma tramite `flash`.
        - Eventuali eccezioni durante il processo di eliminazione vengono catturate e gestite, con un messaggio di errore visualizzato tramite `flash`.
    """
    
    if 'authenticated' in session:

        if request.method == 'DELETE':
            # Gestione dell'Eliminazione del Menu
            try:
                menu = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(id_menu)
                service_t_MenuServiziAssociazione.delete_per_menu(id_menu, utenteCancellazione=session.get('username'))
                flash('Menu eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content
            except Exception as e:
                print(f"Error deleting menu: {e}")
                flash('Errore durante l\'eliminazione del menu.', 'danger')
                return '', 400  # Status code 400 Bad Request
        

    else:
        flash('Per favore, effettua il login prima.', 'warning')
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/menu/dettagli/<int:id_menu>', methods=['GET', 'POST'])
def menu_dettagli(id_menu):
    """
    Gestisce le operazioni di visualizzazione e modifica dei dettagli di un menu specifico.

    Questa funzione consente di:
    - Recuperare i dettagli di un menu esistente tramite l'ID specificato.
    - Modificare le associazioni di piatti e preparazioni per un menu esistente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli del menu e le associazioni esistenti di piatti e preparazioni.
    - **POST**: Aggiorna le associazioni di piatti e preparazioni per il menu specificato utilizzando i dati forniti nel modulo.

    Args:
        id_menu (int): L'ID del menu da gestire.

    Returns:
        Response:
            - **GET**:
                - Rende il template 'dettaglio_menu.html' con i dettagli del menu, le associazioni di piatti e preparazioni, e i relativi moduli.
                - Redirect alla pagina di login se l'utente non è autenticato.
            - **POST**:
                - Redirect alla pagina del menu se l'aggiornamento ha successo.
                - JSON con un messaggio di errore se ci sono problemi durante l'aggiornamento.
                - Status code 500 in caso di errore durante l'operazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Il modulo consente di selezionare piatti e preparazioni, e salva le associazioni nel database.
        - Viene gestito il logging per eventuali errori durante le operazioni.
    """

    if 'authenticated' in session:
        # Recupera le associazioni esistenti
        associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(id_menu)


        menu_servizio = service_t_MenuServizi.get_by_id(id_menu)
        menu_giorno = service_t_Menu.get_by_id(menu_servizio['fkMenu'])
        servizi = service_t_Servizi.get_all_servizi()

        servizi_map = {int(servizo['id']): servizo['descrizione'] for servizo in servizi}

        piatti_e_prep = []
        for associazione in associazioni:
            piatti_e_prep.extend(service_t_AssociazionePiattiPreparazionie.get_by_id_ritorno_diz(associazione['id']))

        tipologia_piatti = service_t_TipiPiatti.get_all_in_menu()
        piatti = service_t_Piatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()

        prep_per_piatto = []
        for piatto in piatti:
            prep = service_t_AssociazionePiattiPreparazionie.get_preparazione_by_piatto(piatto['id'])       
            associazione = {
                'piatto': piatto,
                'preparazioni': prep
            }        
            prep_per_piatto.append(associazione)

        form = MenuForm()
        form.piatti.choices = [(piatto['id'], piatto['titolo']) for piatto in piatti]
        form.preparazioni.choices = [(preparazione['id'], preparazione['descrizione']) for preparazione in preparazioni]

        # Imposta i valori di default per i campi del form
        selected_piatti_ids = [item['fkPiatto'] for item in piatti_e_prep]
        selected_preparazioni_ids = [item['fkPreparazione'] for item in piatti_e_prep]
        form.piatti.default = selected_piatti_ids
        form.preparazioni.default = selected_preparazioni_ids
        form.process()

        piatti_to_preparazioni = {piatto['id']: [] for piatto in piatti}
        for assoc in piatti_e_prep:
            piatti_to_preparazioni[assoc['fkPiatto']].append(assoc['fkPreparazione'])

        piatti_map = {int(piatto['id']): piatto['titolo'] for piatto in piatti}
        codice_map = {int(piatto['id']): piatto['codice'] for piatto in piatti}
        preparazioni_map = {int(preparazione['id']): preparazione['descrizione'] for preparazione in preparazioni}

        if form.validate_on_submit():
            app.logger.debug("Form valido.")
            
            
            # Raccogli le associazioni selezionate dall'utente
            piatto_e_prep = []
            for piatto_id in request.form.getlist('piatti'):
                preparazioni_ids = request.form.getlist(f'preparazioni-{piatto_id}')
                for preparazione_id in preparazioni_ids:
                    piatto_e_prep.append({
                        'fkPiatto': piatto_id,
                        'fkPreparazione': preparazione_id
                    })

            associazioni_id = []
            for assoc in piatto_e_prep:
                result = service_t_AssociazionePiattiPreparazionie.get_id_by_preparazione_e_piatto(assoc['fkPiatto'], assoc['fkPreparazione'])
                if 'Error' in result:
                    app.logger.error(f"Errore durante il recupero dell'associazione: {result['Error']}")
                    return {'Error': result['Error']}, 500
                associazioni_id.append(result['id'])
            # Elenco delle nuove associazioni da inserire
            try:
                # Elimina le associazioni esistenti
                if associazioni:
                    service_t_MenuServiziAssociazione.delete_per_menu(fkMenuServizio=id_menu, utenteCancellazione=session.get('username'))
               
                # Crea le nuove associazioni
                for assoc_id in associazioni_id:
                    response = service_t_MenuServiziAssociazione.create(
                        fkMenuServizio=id_menu,
                        fkAssociazione=assoc_id,
                        utenteInserimento=session.get('username')
                    )

                    if 'Error' in response:
                        app.logger.error(f"Errore durante l'inserimento dell'associazione: {response['Error']}")
                        return {'Error': response['Error']}, 500
                
                app.logger.debug("Menu modificato con successo nel database.")
                return redirect(url_for('app_cucina.menu'))#qui devo passare il menu e il mese corrente
            except Exception as e:
                app.logger.error(f"Errore durante la modifica del menu: {str(e)}")
                return {'Error': str(e)}, 500
        else:
            app.logger.debug("Form non valido: {}".format(form.errors))

        # Renderizza il template se il form non è stato sottomesso con successo
        return render_template(
            'dettaglio_menu.html', 
            form=form,
            preparazioni=preparazioni,
            piatti_map=piatti_map,
            preparazioni_map=preparazioni_map,
            piatti=piatti,
            tipologia_piatti=tipologia_piatti,
            piatti_to_preparazioni=piatti_to_preparazioni,
            prep_per_piatto=prep_per_piatto,
            codice_map=codice_map,
            menu_servizio=menu_servizio,
            menu_giorno=menu_giorno,
            servizi_map=servizi_map
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/schede', methods=['GET', 'POST'])
def schede():
    """
    Gestisce la visualizzazione e la creazione di schede.

    Questa funzione consente di:
    - Visualizzare l'elenco delle schede esistenti.
    - Creare una nuova scheda con dettagli specifici.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza tutte le schede e i tipi di menu e alimentazione disponibili.
    - **POST**: Crea una nuova scheda se il modulo è stato inviato e validato con successo.

    Args:
        Nessuno. Le informazioni sulle schede sono gestite attraverso i dati di sessione e il modulo.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'schede.html' con i seguenti dati:
                    - Elenco delle schede esistenti.
                    - Mappa dei tipi di menu e dei tipi di alimentazione disponibili.
                    - Form per inserire una nuova scheda.
            - **POST**:
                - Se il modulo è valido, crea una nuova scheda e reindirizza alla pagina aggiornata delle schede.
                - Visualizza un messaggio di conferma tramite `flash`.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come schede, tipi di menu e tipi di alimentazione.
        - Il form per le schede consente di selezionare tipi di menu e alimentazione, e di inserire dettagli come nome, titolo, descrizione, date, e note.
    """  
    if 'authenticated' in session:
        schede = service_t_Schede.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_alimentazione = service_t_TipiAlimentazione.get_all()

        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        tipi_alimentazione_map = {int(tipi_alimentazione['id']): tipi_alimentazione['descrizione'] for tipi_alimentazione in tipi_alimentazione}

        form = schedaForm()

        form.fkTipoAlimentazione.choices = [(tipo_alimentazione['id'], tipo_alimentazione['descrizione']) for tipo_alimentazione in tipi_alimentazione]
        form.fkTipoMenu.choices = [(tipo_menu['id'], tipo_menu['descrizione']) for tipo_menu in tipi_menu]

        if form.validate_on_submit():

            # Inserimento dei dati nel database
            service_t_Schede.create(
                fkTipoAlimentazione=form.fkTipoAlimentazione.data,
                fkTipoMenu=form.fkTipoMenu.data,
                nome=form.nome.data,
                titolo=form.titolo.data,
                sottotitolo=form.sottotitolo.data,
                descrizione=form.descrizione.data,
                backgroundColor=form.backgroundColor.data,
                dipendente=form.dipendente.data,
                note=form.note.data,
                inizio=form.inizio.data,
                fine=form.fine.data,
                nominativa=form.nominativa.data,
                utenteInserimento=session.get('username')
            )

            flash('Scheda aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.schede'))

        return render_template(
            'schede.html',
            schede=schede,
            tipi_menu_map=tipi_menu_map,
            tipi_alimentazione_map=tipi_alimentazione_map,
            form=form,
        )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/schede/<int:id>', methods=['GET', 'POST', 'DELETE'])
def modifica_scheda(id):
    """
    Gestisce le operazioni di visualizzazione, aggiornamento e eliminazione di una scheda specifica.

    Questa funzione consente di:
    - Recuperare i dettagli di una scheda esistente tramite l'ID specificato.
    - Aggiornare i dettagli di una scheda esistente.
    - Eliminare una scheda specificata.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli della scheda e le scelte dei tipi di alimentazione e menu.
    - **POST**: Aggiorna i dettagli della scheda esistente con i dati forniti nel modulo.
    - **DELETE**: Elimina la scheda specificata.

    Args:
        id (int): L'ID della scheda da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli della scheda, inclusi campi come `backgroundColor`, `fkTipoAlimentazione`, `fkTipoMenu`, `nome`, `titolo`, `sottotitolo`, `descrizione`, `dipendente`, `nominativa`, `inizio`, `fine`, e `note`.
                - Redirect alla pagina delle schede se la scheda non viene trovata.
                - Redirect alla pagina di login se l'utente non è autenticato.
            - **POST**:
                - Redirect alla pagina delle schede se l'aggiornamento ha successo.
                - Flash message di successo se l'aggiornamento avviene correttamente.
            - **DELETE**:
                - Status code 204 No Content se la scheda è stata eliminata con successo.
                - Flash message di successo se l'eliminazione avviene correttamente.
                - Status code 400 Bad Request in caso di errore durante l'eliminazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Viene gestito il logging per eventuali errori durante le operazioni.
    """

    if 'authenticated' in session:

        
        if request.method == 'GET':
            scheda = service_t_Schede.get_by_id(id)
            if not scheda:
                flash('Scheda non trovata!', 'danger')
                return redirect(url_for('app_cucina.schede'))
            
            tipi_menu = service_t_TipiMenu.get_all()
            tipi_alimentazione = service_t_TipiAlimentazione.get_all()
            form = schedaForm(obj=scheda)
            

            form.fkTipoAlimentazione.choices = [(tipo_alimentazione['id'], tipo_alimentazione['descrizione']) for tipo_alimentazione in tipi_alimentazione]
            form.fkTipoMenu.choices = [(tipo_menu['id'], tipo_menu['descrizione']) for tipo_menu in tipi_menu]

            return jsonify({
                'backgroundColor': scheda.get('backgroundColor'),
                'fkTipoAlimentazione': scheda.get('fkTipoAlimentazione'),
                'fkTipoMenu': scheda.get('fkTipoMenu'),
                'nome': scheda.get('nome'),
                'titolo': scheda.get('titolo'),
                'sottotitolo': scheda.get('sottotitolo'),
                'descrizione': scheda.get('descrizione'),
                'dipendente': scheda.get('dipendente'),
                'nominativa': scheda.get('nominativa'),
                'inizio': scheda.get('inizio').strftime('%Y-%m-%d') if scheda.get('inizio') else '',
                'fine': scheda.get('fine').strftime('%Y-%m-%d') if scheda.get('fine') else '',
                'note': scheda.get('note')
            })
        
        if request.method == 'POST':
            # Aggiornamento dei dati nel database

            form = schedaForm()
            service_t_Schede.update(
                id=id,
                fkTipoAlimentazione=form.fkTipoAlimentazione.data,
                fkTipoMenu=form.fkTipoMenu.data,
                nome=form.nome.data,
                titolo=form.titolo.data,
                sottotitolo=form.sottotitolo.data,
                descrizione=form.descrizione.data,
                backgroundColor=form.backgroundColor.data,
                dipendente=form.dipendente.data,
                note=form.note.data,
                inizio=form.inizio.data,
                fine=form.fine.data,
                nominativa=form.nominativa.data,
                utenteInserimento=session.get('username')
            )

            flash('Scheda aggiornata con successo!', 'success')
            return redirect(url_for('app_cucina.schede'))
        

    if request.method == 'DELETE':
        print(f"Request to delete scheda with ID: {id}")  # Aggiungi questo log
        try:
            service_t_Schede.delete(id=id, utenteCancellazione=session.get('username'))
            flash('Scheda eliminata con successo!', 'success')
            return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
        except Exception as e:
            print(f"Error deleting scheda: {e}")  # Log per l'errore
            flash('Errore durante l\'eliminazione della scheda.', 'danger')
            return '', 400  # Status code 400 Bad Request per errori


    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/schede/piatti/<int:id>', methods=['GET', 'POST'])
def schede_piatti(id):
    """
    Gestisce la visualizzazione e la creazione di piatti per una specifica scheda.

    Questa funzione consente di:
    - Visualizzare i piatti associati a una scheda specifica.
    - Aggiungere un nuovo piatto alla scheda per un determinato servizio.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza i piatti associati alla scheda specificata e i dettagli correlati.
    - **POST**: Aggiunge un nuovo piatto alla scheda se il modulo è stato inviato e validato con successo.

    Args:
        id (int): L'ID della scheda per cui visualizzare o aggiungere piatti.

    Query Parameters:
        servizio (int, optional): L'ID del servizio associato ai piatti da visualizzare o aggiungere (default è '1').

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'schede_piatti.html' con i seguenti dati:
                    - Dettagli sulla scheda specificata.
                    - Elenco di piatti disponibili.
                    - Elenco di piatti associati alla scheda (esclusi dolci).
                    - Elenco di dolci associati alla scheda.
                    - Mappa dei tipi di piatti e dei tipi di menu disponibili.
                    - Form per inserire un nuovo piatto.
            - **POST**:
                - Se il modulo è valido, aggiunge un nuovo piatto alla scheda e reindirizza alla pagina aggiornata dei piatti della scheda.
                - Visualizza un messaggio di conferma tramite `flash` in caso di successo o di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come schede, piatti, servizi e tipi di piatti.
        - Il form per i piatti consente di selezionare un piatto, aggiungere note e specificare l'ordinatore.
        - In caso di errore durante l'aggiunta di un piatto, viene registrato l'errore nei log dell'applicazione.
    """  
    if 'authenticated' in session:
        
        servizio_corrente = request.args.get('servizio', '1')
        
        
        # Retrieve data
        scheda = service_t_Schede.get_by_id(id)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(id, servizio_corrente)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(id, servizio_corrente)
        servizi = service_t_Servizi.get_all_servizi()
        tipi_piatti = service_t_TipiPiatti.get_all()

        # Map the data for use in the template
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        piatti_map = {int(piatto['id']): {'titolo': piatto['titolo'], 'codice': piatto['codice'], 'fkTipoPiatto': piatto['fkTipoPiatto']} for piatto in piatti}
        
        # Initialize the form and set its choices
        form = schedaPiattiForm()
        form.piatti.choices = [(piatto['id'], piatto['titolo']) for piatto in piatti]

        if form.validate_on_submit():
            try:
                # Retrieve selected piatto info
                piatto_id = form.piatti.data
                infopiatto = service_t_Piatti.get_by_id(piatto_id)  # Correct method to get piatto info
                
                # Determine the colonna based on fkTipoPiatto
                colonna = 1 if infopiatto['fkTipoPiatto'] < 4 else 2

                service_t_SchedePiatti.create(
                    fkScheda=id, 
                    fkServizio=servizio_corrente, 
                    fkPiatto=piatto_id, 
                    colonna=colonna,
                    riga=0,  # Adjust riga if necessary
                    note=form.note.data,
                    ordinatore=form.ordinatore.data,
                    utenteInserimento=session.get('username')
                )
                
                flash('Scheda aggiunta con successo!', 'success')
                return redirect(url_for('app_cucina.schede_piatti', id=id, servizio=servizio_corrente))
            except Exception as e:
                flash(f'Errore durante l\'aggiunta della scheda: {str(e)}', 'danger')
                # Potresti anche loggare l'eccezione se necessario
                app.logger.error(f'Errore: {str(e)}')

        return render_template(
            'schede_piatti.html',
            scheda=scheda,
            piatti=piatti,
            servizi=servizi,
            schedePiatti=schedePiatti,
            tipi_piatti=tipi_piatti,
            piatti_map=piatti_map,
            tipi_menu_map=tipi_menu_map,
            schedeDolci=schedeDolci,
            form=form
        )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/schede/piatti/info/<int:id_scheda>/<int:id_piatto_scheda>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def modifica_piatti_scheda(id_scheda, id_piatto_scheda):
    """
    Gestisce le operazioni di visualizzazione, aggiunta, eliminazione e modifica di piatti all'interno di una scheda.

    Questa funzione consente di:
    - Recuperare i dettagli di un piatto specifico in una scheda.
    - Aggiungere un nuovo piatto alla scheda, eliminando prima il piatto esistente.
    - Modificare un piatto esistente, impostando un piatto vuoto.
    - Eliminare un piatto specificato dalla scheda.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce i dettagli del piatto specificato.
    - **POST**: Aggiunge un nuovo piatto alla scheda, dopo aver eliminato il piatto esistente.
    - **PUT**: Modifica un piatto esistente impostando un piatto vuoto.
    - **DELETE**: Elimina il piatto specificato dalla scheda.

    Args:
        id_scheda (int): L'ID della scheda contenente il piatto.
        id_piatto_scheda (int): L'ID del piatto da gestire.

    Returns:
        Response:
            - **GET**:
                - JSON contenente i dettagli del piatto, inclusi campi come `piatti`, `note` e `ordinatore`.
                - Status code 404 se il piatto non viene trovato.
                - Status code 500 in caso di errore interno.
            - **POST**:
                - Redirect alla pagina dei piatti della scheda se l'aggiunta ha successo.
                - Flash message di successo se l'aggiunta avviene correttamente.
                - Flash message di errore in caso di problemi durante l'aggiunta.
            - **PUT**:
                - Status code 204 No Content se la modifica del piatto avviene con successo.
                - Flash message di errore in caso di problemi durante la modifica.
            - **DELETE**:
                - Status code 204 No Content se il piatto è stato eliminato con successo.
                - Flash message di successo se l'eliminazione avviene correttamente.
                - Flash message di errore in caso di problemi durante l'eliminazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Viene fornito un sistema di flash messages per comunicare il successo o il fallimento delle operazioni agli utenti.
        - La funzione include logging per monitorare eventuali errori che possono verificarsi durante l'esecuzione delle operazioni.
    """

    if 'authenticated' in session:
        servizio_corrente = request.args.get('servizio', '1')

        if request.method == 'GET':
            try:
                schedaPiatto = service_t_SchedePiatti.get_by_id(id_piatto_scheda)
                if not schedaPiatto:
                    return jsonify({'error': 'Piatto non trovato!'}), 404

                piatti = service_t_Piatti.get_all()
                form = schedaPiattiForm(obj=schedaPiatto)
                form.piatti.choices = [(piatto['id'], piatto['titolo']) for piatto in piatti]

                return jsonify({
                    'piatti': schedaPiatto.get('fkPiatto'),  # Corretto per restituire il valore del piatto
                    'note': schedaPiatto.get('note'),
                    'ordinatore': schedaPiatto.get('ordinatore')
                })
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        if request.method == 'POST':
            try:
                form = schedaPiattiForm()
                service_t_SchedePiatti.delete_piatto_singolo(id=id_piatto_scheda, utenteCancellazione=session.get('username'))

                piatto_id = form.piatti.data
                infopiatto = service_t_Piatti.get_by_id(piatto_id)
                colonna = 1 if infopiatto['fkTipoPiatto'] < 4 else 2

                service_t_SchedePiatti.create(
                    fkScheda=id_scheda, 
                    fkServizio=servizio_corrente,
                    fkPiatto=piatto_id, 
                    colonna=colonna,
                    riga=0,
                    note=form.note.data,
                    ordinatore=form.ordinatore.data,
                    utenteInserimento=session.get('username')
                )

                flash('Scheda aggiunta con successo!', 'success')
                return redirect(url_for('app_cucina.schede_piatti', id=id_scheda, servizio=servizio_corrente))
            except Exception as e:
                flash(f'Errore durante l\'aggiunta della scheda: {str(e)}', 'danger')
                # Potresti anche loggare l'eccezione se necessario
                app.logger.error(f'Errore: {str(e)}')

        

        if request.method == 'PUT':
            print(f"Request to delete scheda with ID: {id_piatto_scheda}")  # Aggiungi questo log
            try:
                service_t_SchedePiatti.crea_piatto_vuoto(id=id_piatto_scheda)
                flash('successo!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori
            

        if request.method == 'DELETE':
            print(f"Request to delete scheda with ID: {id_piatto_scheda}")  # Aggiungi questo log
            try:
                service_t_SchedePiatti.delete_piatto_singolo(id=id_piatto_scheda, utenteCancellazione=session.get('username'))
                flash('piatto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori

    else:
        return redirect(url_for('app_cucina.login'))
    


@app_cucina.route('/ordini/brodi', methods=['POST'])
def update_scheda_count():
    """
    Gestisce l'aggiornamento del conteggio delle schede associate a un ordine per i brodi.

    Questa funzione consente di:
    - Aggiornare il conteggio totale dei brodi per un determinato reparto all'interno di un ordine.
    - Creare nuove schede di ordine per i brodi, eliminando eventuali schede precedenti associate.

    La funzione esegue le seguenti operazioni a seconda della richiesta POST:
    - Recupera i dati dalla richiesta JSON per l'ID dell'ordine, ID del servizio, ID del reparto, ID della scheda e il nuovo conteggio.
    - Se esistono già schede di brodo associate all'ordine, queste vengono eliminate.
    - Crea un numero di nuove schede di ordine per i brodi pari al conteggio specificato.

    Args:
        Nessuno. I dati per l'aggiornamento sono forniti nel corpo della richiesta JSON.

    Request Body (JSON):
        {
            "ordineId": int,        # ID dell'ordine da aggiornare
            "servizioId": int,      # ID del servizio associato
            "reparto_id": int,      # ID del reparto
            "scheda_id": int,       # ID della scheda di brodo
            "new_count": int         # Nuovo conteggio di schede di brodo da creare
        }

    Returns:
        Response:
            - **POST**:
                - Ritorna un oggetto JSON che indica il successo dell'operazione.
                - In caso di errore, ritorna un oggetto JSON con un messaggio di errore e codice di stato 500.

    Notes:
        - Se l'utente non è autenticato, l'operazione potrebbe fallire a causa di problemi di autorizzazione.
        - Viene eseguito un inserimento unico del totale dei brodi per l'intero reparto.
        - È prevista la gestione delle eccezioni per garantire la stabilità del servizio e il corretto logging degli errori.
        - La scheda brodi viene gestita in maniera diversa rispetto alle altre schede.  
            Aggiorna il conteggio delle schede associate a un ordine per i brodi.
            viene fatto un inserimento unico del totale dei brodi per l'intero reparto.
    """
    try:
        # Recupera i dati dalla richiesta JSON
        data = request.get_json()

        ordine_id = data.get('ordineId')
        servizio_id = data.get('servizioId')
        reparto_id = data.get('reparto_id')
        scheda_id = data.get('scheda_id')
        new_count = data.get('new_count')

        # Ottieni i dati dell'ordine
        get_data = service_t_Ordini.get_by_id(ordine_id)
        ordine_data = get_data['data']

        brodi = service_t_OrdiniSchede.get_all_by_day_and_reparto(ordine_data, reparto_id, servizio_id, scheda_id)
        if brodi:
            for brodo in brodi:
                service_t_OrdiniPiatti.delete_by_fkOrdine(brodo['id'])
                service_t_OrdiniSchede.delete(brodo['id'], utenteCancellazione=session.get('username'))


        # Aggiorna o crea i dati della scheda
        for _ in range(int(new_count)):  # Usa il conteggio per determinare quante schede creare
            new_scheda_ordine = service_t_OrdiniSchede.create(
                fkOrdine=ordine_id,
                fkReparto=reparto_id,
                data=ordine_data,
                fkServizio=servizio_id,
                fkScheda=scheda_id,
                cognome='*',
                nome='*',
                letto=None,
                utenteInserimento=session.get('username')
            )

            # Inserisci il piatto fisso
            try:
                service_t_OrdiniPiatti.create(
                    fkOrdineScheda=new_scheda_ordine,
                    fkPiatto=21,  # ID fisso del piatto "brodo"
                    quantita=1,   # Quantità fissa
                    note=None
                )
            except (ValueError, KeyError) as e:
                print(f"Error processing ordine piatti: {e}")

        return jsonify({'success': True})

    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({'success': False, 'message': 'Errore interno del server'}), 500


@app_cucina.route('/ordini/schede_piatti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>', methods=['GET', 'POST'])
@app_cucina.route('/ordini/schede_piatti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>/<int:ordine_id>', methods=['GET', 'POST'])
def ordine_schede_piatti(id, servizio, reparto, scheda, ordine_id=None):
    """
    Gestisce la visualizzazione e la creazione di ordini di piatti per una scheda specifica.

    Questa funzione consente di:
    - Visualizzare i dettagli degli ordini di piatti per un determinato giorno, servizio e scheda.
    - Creare un nuovo ordine di piatti, se non esiste già un ordine per il giorno e il servizio specificati.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza i dettagli degli ordini di piatti per il giorno, servizio, reparto e scheda selezionati.
    - **POST**: Crea un nuovo ordine di piatti se non ne esiste già uno per il giorno e il servizio selezionati.

    Args:
        id (int): L'ID dell'ordine principale.
        servizio (int): L'ID del servizio (ad esempio colazione, pranzo).
        reparto (int): L'ID del reparto per cui si sta creando l'ordine.
        scheda (int): L'ID della scheda per cui si stanno ordinando i piatti.
        ordine_id (int, optional): L'ID dell'ordine di scheda specifico (default è None).

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'ordine_schede_piatti.html' con i seguenti dati:
                    - Dettagli sull'ordine principale per la data e il servizio specificati.
                    - Informazioni su piatti non dolci e dolci, schede, tipi di menu e reparti.
                    - Form per inserire un nuovo ordine di piatti.
                    - Dati aggregati sugli ordini, come i dettagli degli utenti e dei piatti.
                    - aggiunto calcolo delle calorie dei piatti e dell'intero menu (bisogna però inserire gli ingredienti in tutte le preparazioni)
                    - aggiunto lista degli allergeni presenti nei piatti
            - **POST**:
                - Se un ordine non esiste già per il giorno e il servizio selezionati, ne viene creato uno nuovo.
                - Reindirizza alla pagina aggiornata degli ordini con un messaggio di successo.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come piatti, schede, tipi di menu, e informazioni sul servizio e reparto.
        - È previsto un controllo sui tempi di ordine per evitare ordini effettuati dopo le 10 del mattino per il giorno successivo.
        - Il form per l'ordine consente di selezionare i piatti e di specificare la quantità e eventuali note aggiuntive.
    """
    if 'authenticated' in session:
        
        # Recupera i dati necessari
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(scheda, servizio)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(scheda, servizio)
        get_data = service_t_Ordini.get_by_id(id)
        scheda = service_t_Schede.get_by_id(scheda)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        info_servizio = service_t_Servizi.get_servizio_by_id(servizio)
        info_reparto = service_t_Reparti.get_by_id(reparto)
        tipi_piatti = service_t_TipiPiatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()  # Recupera tutte le preparazioni
        allergeni = service_t_Allergeni.get_all()

        # Costruisci una mappa delle preparazioni
        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        allergeni_map = {str(allergene['id']): allergene['nome'] for allergene in allergeni}

        ordine_data = get_data['data']
        year = ordine_data.year
        month = ordine_data.month
        day = ordine_data.day

        preparazioni_map = get_preparazioni_map(get_data['data'], scheda['fkTipoMenu'], servizio)
        

        def calculate_preparations_calories(preparations_map):
            calories_data = {}
            for p_id, p_name in preparations_map.items():
                print(p_id, p_name)
                # Ottieni i dati delle calorie usando l'ID o il nome del piatto
                prep_calorie = service_t_preparazioni.recupero_totale_ingredienti_base(p_name)  # O usa p_id se necessario
                # Stampa di debug per verificare il risultato
                print(f"Calorie info per {p_name} (ID: {p_id}): {prep_calorie}")
                
                # Assicurati che prep_calorie contenga i dati necessari
                if prep_calorie:  # Se ci sono dati disponibili
                    calories_data[p_id] = {  # Usa l'ID come chiave
                        'calorie_totali': round(prep_calorie.get('calorie_totali', 0)), 
                        'allergeni': prep_calorie.get('allergeni', 'Non disponibili')
                    }
                else:
                    calories_data[p_id] = {
                        'calorie_totali': 0,
                        'allergeni': 'Non disponibili'
                    }
            return calories_data


        
        prep_calorie_data = calculate_preparations_calories(preparazioni_map)

        

        form = ordineSchedaForm()
        
        piatti_map = {}
        for piatto in piatti:
            piatto_id = int(piatto['id'])
            tipo_piatto = piatto['fkTipoPiatto']
            
            # Filtra solo i piatti (preparazioni) che fanno parte del menu
            
            if piatto_id in preparazioni_map:
                piatti_map[piatto_id] = {
                    'id': piatto['id'],
                    'titolo': preparazioni_map.get(piatto_id, piatto['titolo']), # Usa solo la descrizione della preparazione
                    'codice': piatto['codice'],
                    'fkTipoPiatto': piatto['fkTipoPiatto']
                }

        # Assegna piatti_map alla scheda corrente
        scheda['piatti'] = piatti_map

        # Recupera i dettagli dell'ordine per il giorno e il reparto specifico
        dettagli_ordine = service_t_OrdiniSchede.get_all_by_day_and_reparto(ordine_data, reparto, servizio, scheda['id'])

        # Lista di tutti gli ID disponibili, escludendo la scheda vuota (0)
        lista_id_disponibili = [ordine['id'] for ordine in dettagli_ordine if ordine['id'] != 0]

        # Aggiungi sempre l'ordine con ID 0 come ultimo elemento se c'è un nuovo ordine
        lista_id_disponibili.append(0)

        # Gestione dell'ordine_id e current_scheda_index
        if ordine_id is None or ordine_id == 0:
            # Nuovo ordine, quindi è il nuovo elemento nella lista
            ordine_id = 0
            current_scheda_index = len(lista_id_disponibili) - 1
            info_utente = {'nome': '', 'cognome': '', 'letto': '', 'note': ''}
            info_piatti = []
            # Precedente ordine è l'ultimo dell'elenco, escludendo ID 0
            prev_order_id = lista_id_disponibili[-2] if len(lista_id_disponibili) > 1 else None
            next_order_id = None
        else:
            if ordine_id not in lista_id_disponibili:
                ordine_id = lista_id_disponibili[-1]  # Imposta ordine_id come l'ultimo valido

            current_index = lista_id_disponibili.index(ordine_id)
            prev_order_id = lista_id_disponibili[current_index - 1] if current_index > 0 else None
            # Il next_order_id non deve includere 0 se l'utente sta visualizzando un ordine esistente
            next_order_id = lista_id_disponibili[current_index + 1] if current_index < len(lista_id_disponibili) - 2 else None  # Ignora l'ultimo 0
            current_scheda_index = current_index

            info_utente = service_t_OrdiniSchede.get_by_id(ordine_id)
            info_piatti = service_t_OrdiniPiatti.get_all_by_ordine_scheda(ordine_id)

        if form.validate_on_submit():

                     # Time limit check
            if not check_order_time_limit(get_data['data']):
                flash("Non è possibile effettuare ordini per il giorno successivo dopo le 10 del mattino.", 'error')
                return redirect(url_for('app_cucina.ordini'))

            fkOrdine = id
            fkReparto = reparto
            data = get_data['data']
            fkServizio = servizio
            fkScheda = scheda['id']
            letto = form.letto.data

            ordine_id = request.form.get('ordine_id', default=None, type=int)
        
            if ordine_id is None or ordine_id == 0:
                letto_occupato = service_t_OrdiniSchede.check_letto(fkOrdine, fkReparto, data, fkServizio, letto)
                if letto_occupato:
                    flash(f"il letto numero {letto} è gia occupato.", 'error')
                    return redirect(url_for('app_cucina.ordine_schede_piatti', id=id, servizio=servizio, reparto=reparto, scheda=scheda['id']))
                        
            if ordine_id and ordine_id != 0:
                service_t_OrdiniPiatti.delete_by_fkOrdine(ordine_id)
                service_t_OrdiniSchede.delete(ordine_id, utenteCancellazione=session.get('username'))

            # Creazione di un nuovo ordine
            new_scheda_ordine = service_t_OrdiniSchede.create(
                fkOrdine=id,
                fkReparto=reparto,
                data=data,
                fkServizio=servizio,
                fkScheda=fkScheda,
                cognome=form.cognome.data,
                nome=form.nome.data,
                letto=letto,
                utenteInserimento=session.get('username')
            )

            piatti_list = json.loads(request.form['piattiList'])
            for piatto in piatti_list:
                try:
                    service_t_OrdiniPiatti.create(
                        fkOrdineScheda=new_scheda_ordine,
                        fkPiatto=int(piatto['fkPiatto']),
                        quantita=int(piatto['quantita']),
                        note=str(piatto['note']),
                    )
                    print(f"ordine piatti saved: {piatto}")
                except (ValueError, KeyError) as e:
                    print(f"Error processing ordine piatti: {piatto}, error: {e}")

            flash('Preparazione aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.ordini', year=year, month=month, day=day, servizio=servizio))


        return render_template(
            'ordine_schede_piatti.html',
            id=id,
            scheda=scheda,
            piatti=piatti,
            schedePiatti=schedePiatti,
            tipi_piatti=tipi_piatti,
            piatti_map=piatti_map,
            tipi_menu_map=tipi_menu_map,
            schedeDolci=schedeDolci,
            info_reparto=info_reparto,
            info_servizio=info_servizio,
            form=form,
            servizio=servizio,
            prev_order_id=prev_order_id,
            next_order_id=next_order_id,
            total_schede=len(lista_id_disponibili) -1 ,
            current_scheda_index=current_scheda_index +1,
            reparto=reparto,
            dettagli_ordine=dettagli_ordine,
            info_utente=info_utente,
            info_piatti=info_piatti,
            ordine_id=ordine_id,
            year=year,
            month=month,
            allergeni_map=allergeni_map,
            prep_calorie_data=prep_calorie_data,
            day=day
        )
    else:
        return redirect(url_for('app_cucina.login'))
    


@app_cucina.route('/ordini/schede_dipendenti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>', methods=['GET', 'POST'])
@app_cucina.route('/ordini/schede_dipendenti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>/<int:ordine_id>', methods=['GET', 'POST'])
def schede_dipendenti(id, servizio, reparto, scheda, ordine_id=None):
    """
    Gestisce la visualizzazione e la creazione di ordini di piatti per una scheda specifica.

    Questa funzione consente di:
    - Visualizzare i dettagli degli ordini di piatti per un determinato giorno, servizio e scheda.
    - Creare un nuovo ordine di piatti, se non esiste già un ordine per il giorno e il servizio specificati.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza i dettagli degli ordini di piatti per il giorno, servizio, reparto e scheda selezionati.
    - **POST**: Crea un nuovo ordine di piatti se non ne esiste già uno per il giorno e il servizio selezionati.

    Args:
        id (int): L'ID dell'ordine principale.
        servizio (int): L'ID del servizio (ad esempio colazione, pranzo).
        reparto (int): L'ID del reparto per cui si sta creando l'ordine.
        scheda (int): L'ID della scheda per cui si stanno ordinando i piatti.
        ordine_id (int, optional): L'ID dell'ordine di scheda specifico (default è None).

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'ordini_schede_dipendenti_totali.html' con i seguenti dati:
                    - Dettagli sull'ordine principale per la data e il servizio specificati.
                    - Informazioni su piatti non dolci e dolci, schede, tipi di menu e reparti.
                    - Form per inserire un nuovo ordine di piatti.
                    - Dati aggregati sugli ordini, come i dettagli degli utenti e dei piatti.
            - **POST**:
                - Se un ordine non esiste già per il giorno e il servizio selezionati, ne viene creato uno nuovo.
                - Reindirizza alla pagina aggiornata degli ordini con un messaggio di successo.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come piatti, schede, tipi di menu, e informazioni sul servizio e reparto.
        - È previsto un controllo sui tempi di ordine per evitare ordini effettuati dopo le 10 del mattino per il giorno successivo.
        - Il form per l'ordine consente di selezionare i piatti e di specificare la quantità e eventuali note aggiuntive.
    """
    if 'authenticated' in session:
        
        # Recupera i dati necessari
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(scheda, servizio)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(scheda, servizio)
        get_data = service_t_Ordini.get_by_id(id)
        scheda = service_t_Schede.get_by_id(scheda)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        info_servizio = service_t_Servizi.get_servizio_by_id(servizio)
        info_reparto = service_t_Reparti.get_by_id(reparto)
        tipi_piatti = service_t_TipiPiatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()  # Recupera tutte le preparazioni
        allergeni = service_t_Allergeni.get_all()

        # Costruisci una mappa delle preparazioni
        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        allergeni_map = {str(allergene['id']): allergene['nome'] for allergene in allergeni}

        ordine_data = get_data['data']
        year = ordine_data.year
        month = ordine_data.month
        day = ordine_data.day

        preparazioni_map = get_preparazioni_map(get_data['data'], scheda['fkTipoMenu'], servizio)
            

        form = ordineSchedaDipendentiForm()
        
        piatti_map = {}
        for piatto in piatti:
            piatto_id = int(piatto['id'])
            tipo_piatto = piatto['fkTipoPiatto']
            
            # Filtra solo i piatti (preparazioni) che fanno parte del menu
            
            if  piatto_id in preparazioni_map:
                piatti_map[piatto_id] = {
                    'id': piatto['id'],
                    'titolo': preparazioni_map.get(piatto_id, piatto['titolo']), # Usa solo la descrizione della preparazione
                    'codice': piatto['codice'],
                    'fkTipoPiatto': piatto['fkTipoPiatto']
                }

        # Assegna piatti_map alla scheda corrente
        scheda['piatti'] = piatti_map

        # Recupera i dettagli dell'ordine per il giorno e il reparto specifico
        dettagli_ordine = service_t_OrdiniSchede.get_all_by_day_and_reparto(ordine_data, reparto, servizio, scheda['id'])

        # Lista di tutti gli ID disponibili, escludendo la scheda vuota (0)
        lista_id_disponibili = [ordine['id'] for ordine in dettagli_ordine if ordine['id'] != 0]

        # Aggiungi sempre l'ordine con ID 0 come ultimo elemento se c'è un nuovo ordine
        lista_id_disponibili.append(0)

        # Gestione dell'ordine_id e current_scheda_index
        if ordine_id is None or ordine_id == 0:
            # Nuovo ordine, quindi è il nuovo elemento nella lista
            ordine_id = 0
            current_scheda_index = len(lista_id_disponibili) - 1
            info_utente = {'nome': '', 'cognome': '', 'note': ''}
            info_piatti = []
            # Precedente ordine è l'ultimo dell'elenco, escludendo ID 0
            prev_order_id = lista_id_disponibili[-2] if len(lista_id_disponibili) > 1 else None
            next_order_id = None
        else:
            if ordine_id not in lista_id_disponibili:
                ordine_id = lista_id_disponibili[-1]  # Imposta ordine_id come l'ultimo valido

            current_index = lista_id_disponibili.index(ordine_id)
            prev_order_id = lista_id_disponibili[current_index - 1] if current_index > 0 else None
            # Il next_order_id non deve includere 0 se l'utente sta visualizzando un ordine esistente
            next_order_id = lista_id_disponibili[current_index + 1] if current_index < len(lista_id_disponibili) - 2 else None  # Ignora l'ultimo 0
            current_scheda_index = current_index

            info_utente = service_t_OrdiniSchede.get_by_id(ordine_id)
            info_piatti = service_t_OrdiniPiatti.get_all_by_ordine_scheda(ordine_id)

        if form.validate_on_submit():

                     # Time limit check
            if not check_order_time_limit(get_data['data']):
                flash("Non è possibile effettuare ordini per il giorno successivo dopo le 10 del mattino.", 'error')
                return redirect(url_for('app_cucina.ordini_dipendenti'))

            data = get_data['data']
            fkScheda = scheda['id']
            ordine_id = request.form.get('ordine_id', default=None, type=int)

                
                        
            if ordine_id and ordine_id != 0:
                service_t_OrdiniPiatti.delete_by_fkOrdine(ordine_id)
                service_t_OrdiniSchede.delete(ordine_id, utenteCancellazione=session.get('username'))

            # Creazione di un nuovo ordine
            new_scheda_ordine = service_t_OrdiniSchede.create(
                fkOrdine=id,
                fkReparto=reparto,
                data=data,
                fkServizio=servizio,
                fkScheda=fkScheda,
                cognome=form.cognome.data,
                nome=form.nome.data,
                letto=None,
                utenteInserimento=session.get('username')
            )

            piatti_list = json.loads(request.form['piattiList'])
            for piatto in piatti_list:
                try:
                    service_t_OrdiniPiatti.create(
                        fkOrdineScheda=new_scheda_ordine,
                        fkPiatto=int(piatto['fkPiatto']),
                        quantita=int(piatto['quantita']),
                        note=str(piatto['note']),
                    )
                    print(f"ordine piatti saved: {piatto}")
                except (ValueError, KeyError) as e:
                    print(f"Error processing ordine piatti: {piatto}, error: {e}")

            flash('Preparazione aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.ordini_dipendenti', year=year, month=month, day=day, servizio=servizio))


        return render_template(
            'ordini_schede_dipendenti_totali.html',
            id=id,
            scheda=scheda,
            piatti=piatti,
            schedePiatti=schedePiatti,
            tipi_piatti=tipi_piatti,
            piatti_map=piatti_map,
            tipi_menu_map=tipi_menu_map,
            schedeDolci=schedeDolci,
            info_reparto=info_reparto,
            info_servizio=info_servizio,
            form=form,
            servizio=servizio,
            prev_order_id=prev_order_id,
            next_order_id=next_order_id,
            total_schede=len(lista_id_disponibili) -1 ,
            current_scheda_index=current_scheda_index +1,
            reparto=reparto,
            dettagli_ordine=dettagli_ordine,
            info_utente=info_utente,
            info_piatti=info_piatti,
            ordine_id=ordine_id,
            year=year,
            month=month,
            allergeni_map=allergeni_map,
            day=day
        )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/ordini/print/<int:id>', methods=['GET', 'POST'])
def print_ordini(id):
    """
    Gestisce la visualizzazione e la stampa degli ordini associati a un determinato ID.

    Questa funzione consente di:
    - Recuperare tutti gli ordini associati all'ID fornito per visualizzarli in un formato stampabile.
    - Mostrare informazioni dettagliate sui piatti ordinati, inclusi i preparativi e le schede.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera i dettagli degli ordini per l'ID fornito e li prepara per la visualizzazione in formato stampabile.
    - **POST**: Attualmente non gestito; la funzione è focalizzata sulla visualizzazione.

    Args:
        id (int): L'ID dell'ordine per il quale si desidera visualizzare e stampare i dettagli.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'print_ordini.html' con i seguenti dati:
                    - Dettagli sugli ordini associati all'ID fornito, inclusi i piatti ordinati, le schede e le informazioni sul reparto.
                    - Mappa delle preparazioni associate a ciascun piatto ordinato.
                    - Informazioni sui tipi di menu e schede disponibili per il servizio.
            - **POST**:
                - Non implementato, quindi non restituisce dati.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come ordini, piatti, schede, tipi di menu, e preparazioni.
        - Viene gestita la creazione di mappe per organizzare i dati in modo efficace prima della visualizzazione.
        - La funzione attualmente non gestisce il metodo POST; pertanto, l'attenzione è sulla visualizzazione dei dati.
    """
    if 'authenticated' in session:
        # Recupera tutti gli ordini associati all'ID fornito
        tutti_gli_ordini = service_t_OrdiniSchede.get_all_by_ordine_per_stampa(id)

        tipi_menu = service_t_TipiMenu.get_all()
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        preparazioni = service_t_preparazioni.get_all_preparazioni()
        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}

        ordini_data = []

        for ordine in tutti_gli_ordini:
            # Resetta la lista dei piatti per ogni ordine
            Lista_piatti = []

            schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(ordine['fkScheda'], ordine['fkServizio'])
            schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(ordine['fkScheda'], ordine['fkServizio'])
            scheda = service_t_Schede.get_by_id(ordine['fkScheda'])
            info_reparto = service_t_Reparti.get_by_id(ordine['fkReparto'])
            piatti_ordinati = service_t_OrdiniPiatti.get_all_by_ordine_scheda(ordine['id'])
    
            # Aggiunge i piatti ordinati alla lista dei piatti
            for p in piatti_ordinati:
                piatti = service_t_Piatti.get_by_id(p['fkPiatto'])
                Lista_piatti.append(piatti)

            # Ottieni il menu e i servizi associati
            id_menu = service_t_Menu.get_by_data(ordine['data'], scheda['fkTipoMenu'])
            if 'Error' in id_menu:
                print("Error retrieving menu:", id_menu)
                continue  # Salta questo ordine se c'è un errore
            else:
                menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(id_menu['id'], ordine['fkServizio'])
                
                if isinstance(menu_servizio, dict) and 'id' in menu_servizio:
                    menu_associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_servizio['id'])
                    
                    preparazioni_map = {}  # Inizializza la mappa per ogni ordine

                    for assoc in menu_associazioni:
                        assoc_id = assoc['id'] if isinstance(assoc, dict) else assoc
                        fk_associazione = service_t_AssociazionePiattiPreparazionie.get_by_id(assoc_id)

                        if isinstance(fk_associazione, dict) and 'Error' not in fk_associazione:
                            fk_piatto = fk_associazione['fkPiatto']
                            fk_preparazione = fk_associazione.get('fkPreparazione')
                            descrizione_preparazione = preparazioni_map.get(fk_piatto, service_t_preparazioni.get_descrizione_by_id(fk_preparazione))
                            preparazioni_map[fk_piatto] = descrizione_preparazione
                        else:
                            print(f"Errore nella fk_associazione: {fk_associazione}")

            # Crea una mappa per i piatti
            piatti_map = {}
            for piatto in Lista_piatti:
                piatto_id = int(piatto['id'])
                piatti_map[piatto_id] = {
                    'id': piatto['id'],
                    'titolo': preparazioni_map.get(piatto_id, piatto['titolo']),
                    'codice': piatto['codice'],
                    'fkTipoPiatto': piatto['fkTipoPiatto']
                }

            # Aggiunge le informazioni dell'ordine ai dati finali
            ordini_data.append({
                'ordine': ordine,
                'scheda': scheda,
                'info_reparto': info_reparto,
                'piatti_ordinati': piatti_ordinati,
                'nome': ordine['nome'],
                'cognome': ordine['cognome'],
                'letto': ordine['letto'],
                'schedePiatti': schedePiatti,
                'schedeDolci': schedeDolci,
                'piatti_map': piatti_map
            })

        return render_template('print_ordini.html', 
                               ordini_data=ordini_data,
                               tipi_menu_map=tipi_menu_map)
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/ordini/printProspetto/<int:id>', methods=['GET'])
def print_printProspetto(id):
    """
    (DOBBIAMO IMPLEMENTARE LA DIVISIONE DEI PIATTI)
    Genera e visualizza un prospetto di ordinazione per un determinato ordine.

    Questa funzione consente di:
    - Recuperare e aggregare i dati relativi a un ordine specifico, comprese le schede, i piatti, le preparazioni e i reparti.
    - Presentare un prospetto che mostra il conteggio dei piatti ordinati suddivisi per reparto e preparazione.

    La funzione esegue le seguenti operazioni quando viene effettuata una richiesta **GET**:
    - Recupera l'ordine specificato dall'ID.
    - Recupera tutte le schede associate a quell'ordine.
    - Ottiene informazioni su preparazioni, piatti e reparti disponibili.
    - Raccoglie dati dettagliati sulle preparazioni e i piatti ordinati, aggregando le informazioni per reparto.
    - Calcola i totali per ciascuna preparazione e per l'azienda nel suo complesso.

    Args:
        id (int): L'ID dell'ordine di cui generare il prospetto.

    Returns:
        Response:
            - Mostra la pagina 'printProspetto.html' con i seguenti dati:
                - Mappa delle preparazioni con le loro descrizioni.
                - Conteggi dei piatti ordinati suddivisi per reparto e preparazione.
                - Totali per ogni preparazione e il totale complessivo di piatti ordinati.
                - Mappe dei piatti e dei reparti con le loro descrizioni.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione si basa su diversi servizi per recuperare le informazioni necessarie, tra cui gli ordini, le schede, le preparazioni, i piatti e i reparti.
        - La logica include la gestione delle associazioni tra piatti e preparazioni per garantire un conteggio accurato.
    """
    if 'authenticated' in session:
        # Passo 1: Ottieni i dati dell'ordine, le schede, le preparazioni, i piatti e i reparti
        ordine = service_t_Ordini.get_by_id(id)  # Recupera l'ordine specificato dall'ID
        schede = service_t_OrdiniSchede.get_all_by_ordine(id)  # Recupera tutte le schede associate all'ordine
        preparazioni = service_t_preparazioni.get_all_preparazioni()  # Recupera tutte le preparazioni disponibili
        piatti = service_t_Piatti.get_all()  # Recupera tutti i piatti disponibili
        reparti = service_t_Reparti.get_all()  # Recupera tutti i reparti disponibili

        # Crea mappe per le descrizioni delle preparazioni, reparti e piatti
        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}
        reparti_map = {reparto['id']: reparto['descrizione'] for reparto in reparti}
        piatti_map = {piatto['id']: piatto['titolo'] for piatto in piatti}

        # Inizializza un dizionario per contare i piatti per reparto
        piatti_count = {reparto['id']: {} for reparto in reparti}
        used_preparazioni = set()  # Set per tenere traccia delle preparazioni utilizzate

        # Itera attraverso ogni scheda per raccogliere dati aggiuntivi
        for scheda in schede:
            # Passo 2: Ottieni il giorno e il servizio del menu
            menu_by_scheda = service_t_Schede.get_by_id(scheda['fkScheda'])  # Recupera la scheda del menu
            tipo_menu = service_t_Menu.get_by_data(ordine['data'], menu_by_scheda['fkTipoMenu'])  # Recupera il tipo di menu per la data dell'ordine
            tipo_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio_per_stampa(tipo_menu['id'], ordine['fkServizio'])  # Recupera il servizio associato al menu

            if tipo_servizio:
                tipo_servizio = tipo_servizio[0]  # Prendi il primo tipo di servizio
                piatti_del_menu = service_t_MenuServiziAssociazione.get_info_by_fk_menu_servizio(tipo_servizio['id'])  # Recupera i piatti associati al menu e servizio

                # Estrae le associazioni valide per i piatti del menu
                associazioni_valide = {item['fkAssociazione'] for item in piatti_del_menu}
                piatti_ordinati = service_t_OrdiniPiatti.get_all_by_ordine_scheda(scheda['id'])  # Recupera i piatti ordinati nella scheda

                # Itera attraverso i piatti ordinati
                for piatto_ordinato in piatti_ordinati:
                    fkPiatto = piatto_ordinato['fkPiatto']  # ID del piatto ordinato
                    quantità = piatto_ordinato['quantita']  # Quantità ordinata

                    # Recupera tutte le associazioni di preparazione per il piatto
                    tutte_associazioni = service_t_AssociazionePiattiPreparazionie.get_preparazione_by_piatto(fkPiatto)
                    associazioni_filtrate = [assoc for assoc in tutte_associazioni if assoc['id'] in associazioni_valide]  # Filtra le associazioni valide

                    # Controlla se ci sono associazioni valide per il piatto ordinato
                    for assoc in associazioni_filtrate:
                        fkPreparazione = assoc['fkPreparazione']  # ID della preparazione
                        preparazione_nome = preparazioni_map.get(fkPreparazione, "Non Disponibile")  # Nome della preparazione

                        # Aggiorna il conteggio delle preparazioni per il reparto
                        if preparazione_nome not in piatti_count[scheda['fkReparto']]:
                            piatti_count[scheda['fkReparto']][preparazione_nome] = 0  # Inizializza il conteggio se non esiste
                        piatti_count[scheda['fkReparto']][preparazione_nome] += quantità  # Incrementa la quantità
                        used_preparazioni.add(fkPreparazione)  # Aggiungi la preparazione all'insieme delle preparazioni utilizzate

                    # Se non ci sono associazioni valide, conta il piatto stesso
                    if not associazioni_filtrate:
                        piatto_nome = piatti_map.get(fkPiatto, "Non Disponibile")  # Nome del piatto
                        if piatto_nome not in piatti_count[scheda['fkReparto']]:
                            piatti_count[scheda['fkReparto']][piatto_nome] = 0  # Inizializza il conteggio se non esiste
                        piatti_count[scheda['fkReparto']][piatto_nome] += quantità  # Incrementa la quantità

        # Calcolo dei totali per preparazioni
        preparazioni_totals = {preparazione: 0 for preparazione in set(p for d in piatti_count.values() for p in d.keys())}
        for counts in piatti_count.values():
            for preparazione_nome, count in counts.items():
                if preparazione_nome in preparazioni_totals:
                    preparazioni_totals[preparazione_nome] += count  # Somma le quantità per ogni preparazione

        # Calcolo del totale aziendale
        totale_azienda = sum(count for counts in piatti_count.values() for count in counts.values())  # Somma totale di tutti i piatti

        # Restituisci il template con i dati calcolati
        return render_template(
            'printProspetto.html', 
            preparazioni_map=preparazioni_map,
            piatti_count=piatti_count,
            preparazioni_totals=preparazioni_totals,
            piatti_map=piatti_map,
            reparti_map=reparti_map,
            totale_azienda=totale_azienda
        )
    else:
        # Reindirizza alla pagina di login se non autenticato
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/ordina_pasto', methods=['GET', 'POST'])
def ordina_pasto():
    """
    Gestisce le operazioni per ordinare pasti.

    Questa funzione consente di:
    - Visualizzare e gestire ordini di pasti per un giorno specifico.
    - Creare un nuovo ordine se non esiste già per la data e il servizio corrente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Restituisce la pagina per ordinare pasti, recuperando i dettagli dell'ordine e i piatti disponibili.
    - **POST**: (Non implementato nel codice fornito) Si prevede che gestisca l'invio di un ordine per i pasti.

    Returns:
        Response:
            - **GET**:
                - Rende la pagina `ordina_pasto.html` con tutti i dati necessari per visualizzare e gestire l'ordine dei pasti.
                - Status code 200 OK.
                - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.

    Args:
        - year (int): L'anno per il quale ordinare il pasto. Predefinito è l'anno corrente.
        - month (int): Il mese per il quale ordinare il pasto. Predefinito è il mese corrente.
        - day (int): Il giorno per il quale ordinare il pasto. Predefinito è il giorno corrente.
        - servizio (int): L'ID del servizio corrente. Predefinito è '1'.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione include la creazione di un nuovo ordine se non esiste già per la data specificata e il servizio corrente.
        - Utilizza i servizi per recuperare informazioni sugli utenti, i piatti e i servizi disponibili.
        - La funzione prevede di gestire gli ordini tramite la funzione `processa_ordine` per controllare l'ordine e recuperare informazioni pertinenti.

    Flash Messages:
        - La funzione non gestisce esplicitamente i messaggi flash, ma potrebbe essere implementata in caso di operazioni di ordine (POST).
    """
    if 'authenticated' in session:
        # Imposta la data per domani
        tomorrow = datetime.now() + timedelta(days=1)
        year = request.args.get('year', tomorrow.year, type=int)
        month = request.args.get('month', tomorrow.month, type=int)
        day = request.args.get('day', tomorrow.day, type=int)
        servizio_corrente = request.args.get('servizio', '1')
        
        piatti = service_t_Piatti.get_all()
        # Ottieni i reparti accessibili dall'utente
       
        user = service_t_utenti.get_utente_by_public_id(session['user_id'])
        nome = user['nome']
        cognome = user['cognome']
        data = f'{year}-{month}-{day}'

        # Verifica se esiste già un ordine
        ordine_esistente = service_t_Ordini.existing_Ordine(data, servizio_corrente)
        if not ordine_esistente:
            service_t_Ordini.create(data, servizio_corrente)
            return redirect(url_for('app_cucina.ordina_pasto'))
        
        # Recupera il menu personale e altri dati
        menu_personale = service_t_Schede.get_all_personale()
        servizio = service_t_Servizi.get_all_servizi()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}

        # Elenco delle variabili restituite da processa_ordine
        controllo_ordine, inf_scheda, preparazioni_map, piatti_ordine_map = processa_ordine(data, nome, cognome, servizio_corrente, piatti, menu_personale)

        return render_template(
            'ordina_pasto.html',
            year=year,
            month=month,
            day=day,
            menu_personale=menu_personale,
            servizio_corrente=servizio_corrente,
            reparti=get_user_reparti(session['user_id']),
            servizio=servizio,
            ordine_esistente=ordine_esistente,
            tipi_menu_map=tipi_menu_map,
            preparazioni_map=preparazioni_map,
            controllo_ordine=controllo_ordine,
            inf_scheda=inf_scheda,          
            piatti_ordine_map=piatti_ordine_map
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/ordini/delete/<int:ordine_id>', methods=['DELETE'])
def elimina_ordine_schede_dipendente(ordine_id):
    """
    Gestisce l'eliminazione di un ordine specifico.

    Questa funzione consente di:
    - Eliminare un ordine e i relativi piatti associati in base all'ID dell'ordine fornito.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **DELETE**: Rimuove l'ordine specificato e i piatti associati da database.

    Args:
        ordine_id (int): L'ID dell'ordine da eliminare.

    Returns:
        Response:
            - **DELETE**:
                - Status code 200 OK se l'ordine è stato eliminato con successo.
                - Status code 400 Bad Request se si verifica un errore durante l'eliminazione.
                - Flash message di successo se l'eliminazione avviene correttamente.
                - Flash message di errore in caso di problemi durante l'eliminazione.

    Notes:
        - La funzione verifica se l'utente è autenticato; in caso contrario, reindirizza alla pagina di login.
        - La funzione include un sistema di logging per monitorare eventuali errori che possono verificarsi durante l'eliminazione dell'ordine.
        - Utilizza i servizi per eliminare i piatti associati all'ordine e l'ordine stesso.

    Flash Messages:
        - "ordine eliminato con successo!" per indicare che l'ordine è stato rimosso correttamente.
        - "Errore durante l'eliminazione del ordine." per segnalare un problema durante il processo di eliminazione.
    """
    if 'authenticated' in session:    
           
        try:
            service_t_OrdiniPiatti.delete_by_fkOrdine(ordine_id)
            service_t_OrdiniSchede.delete(ordine_id, utenteCancellazione=session.get('username'))         
            flash('ordine eliminato con successo!', 'success')
            return '', 200  # Status code 200 
        except Exception as e:
            print(f"Error deleting scheda: {e}")  # Log per l'errore
            flash('Errore durante l\'eliminazione del ordine.', 'danger')
            return '', 400  # Status code 400 Bad Request per errori      
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/ordina_pasto/schede_dipendente/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>', methods=['GET', 'POST'])
@app_cucina.route('/ordina_pasto/schede_dipendente/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>/<int:ordine_id>', methods=['GET', 'POST', 'DELETE'])
def ordine_schede_dipendente(id, servizio, reparto, scheda, ordine_id=None):
    """
    Gestisce la visualizzazione e la creazione/modifica degli ordini di schede per i dipendenti.

    Questa funzione consente di:
    - Visualizzare i piatti disponibili per la scheda, il servizio e il reparto selezionati.
    - Creare un nuovo ordine o modificare un ordine esistente per il dipendente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza le informazioni sui piatti, le schede, e i dettagli dell'ordine selezionato.
    - **POST**: Crea un nuovo ordine se non ne esiste già uno per la scheda selezionata, oppure aggiorna un ordine esistente.

    Args:
        id (int): L'ID dell'ordine principale.
        servizio (int): L'ID del servizio (es. colazione, pranzo).
        reparto (int): L'ID del reparto in cui viene effettuato l'ordine.
        scheda (int): L'ID della scheda selezionata per l'ordine.
        ordine_id (int, optional): L'ID dell'ordine da modificare (se presente).

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'ordine_schede_dipendente.html' con i seguenti dati:
                    - Elenco dei piatti disponibili suddivisi in piatti non dolci e dolci.
                    - Dettagli sulla scheda selezionata, tipo di menu e piatti associati.
                    - Informazioni sul servizio e reparto.
                    - Form per inserire o modificare un ordine.
            - **POST**:
                - Se `ordine_id` è fornito e non è zero, modifica l'ordine esistente; altrimenti, crea un nuovo ordine.
                - Reindirizza alla pagina degli ordini aggiornati.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come piatti, schede, e informazioni relative al servizio e reparto.
        - La gestione degli errori del modulo è inclusa per garantire la validità dei dati prima della creazione o modifica dell'ordine.
        - I piatti selezionati e le quantità vengono salvati nel database tramite i rispettivi servizi.
    """
    if 'authenticated' in session:

        # Recupera i dati necessari
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(scheda, servizio)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(scheda, servizio)
        get_data = service_t_Ordini.get_by_id(id)
        scheda = service_t_Schede.get_by_id(scheda)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        info_servizio = service_t_Servizi.get_servizio_by_id(servizio)
        info_reparto = service_t_Reparti.get_by_id(reparto)
        tipi_piatti = service_t_TipiPiatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()  # Recupera tutte le preparazioni

        # Costruisci una mappa delle preparazioni
        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}


        preparazioni_map = get_preparazioni_map(get_data['data'], scheda['fkTipoMenu'], servizio)
        
        piatti_map = {}
        for piatto in piatti:
            piatto_id = int(piatto['id'])
            tipo_piatto = piatto['fkTipoPiatto']
            
            # Filtra solo i piatti (preparazioni) che fanno parte del menu
            # Escludi i tipi di piatti 4 e 5 dal filtraggio
            if tipo_piatto in [4, 5] or piatto_id in preparazioni_map:
                piatti_map[piatto_id] = {
                    'id': piatto['id'],
                    'titolo': preparazioni_map.get(piatto_id, piatto['titolo']), # Usa solo la descrizione della preparazione
                    'codice': piatto['codice'],
                    'fkTipoPiatto': piatto['fkTipoPiatto']
                }

        # Assegna piatti_map alla scheda corrente
        scheda['piatti'] = piatti_map

        info_utente = service_t_OrdiniSchede.get_by_id(ordine_id)
             
        info_piatti = service_t_OrdiniPiatti.get_all_by_ordine_scheda(ordine_id)

        user = service_t_utenti.get_utente_by_public_id(session['user_id'])
        nome = user['nome']
        cognome = user['cognome']

        form = ordinedipendenteForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                piatti_list = json.loads(request.form['piattiList']) 

                # Check if piatti_list is empty or None
                if not piatti_list or len(piatti_list) == 0:
                    flash('Ordine è stato inserito vuoto o non è stato modificato!', 'danger')
                    return redirect(url_for('app_cucina.ordina_pasto', servizio=servizio, reparto=reparto))

                ordine_id = request.form.get('ordine_id', default=None, type=int)

                # Handle existing order if ordine_id is provided
                if ordine_id and ordine_id != 0:
                    service_t_OrdiniPiatti.delete_by_fkOrdine(ordine_id)
                    service_t_OrdiniSchede.delete(ordine_id, utenteCancellazione=session.get('username'))

                # Create a new order
                new_scheda_ordine = service_t_OrdiniSchede.create(
                    fkOrdine=id,
                    fkReparto=reparto,
                    data=get_data['data'],
                    fkServizio=servizio,
                    fkScheda=scheda['id'],
                    cognome=cognome,
                    nome=nome,
                    letto=None,
                    utenteInserimento=session.get('username')
                )

                # Save selected dishes
                for piatto in piatti_list:
                    try:
                        service_t_OrdiniPiatti.create(
                            fkOrdineScheda=new_scheda_ordine,
                            fkPiatto=int(piatto['fkPiatto']),
                            quantita=int(piatto['quantita']),
                            note=str(piatto['note']),
                        )
                        print(f"Ordine piatti salvato: {piatto}")
                    except (ValueError, KeyError) as e:
                        print(f"Errore durante l'elaborazione dell'ordine piatti: {piatto}, errore: {e}")

                flash('Ordine aggiunto con successo!', 'success')
                return redirect(url_for('app_cucina.ordina_pasto', servizio=servizio, reparto=reparto))
            
            else:
                print("Errori del modulo:", form.errors)

        return render_template('ordine_schede_dipendente.html',
            id=id,
            scheda=scheda,
            piatti=piatti,
            schedePiatti=schedePiatti,
            tipi_piatti=tipi_piatti,
            piatti_map=piatti_map,
            tipi_menu_map=tipi_menu_map,
            schedeDolci=schedeDolci,
            info_reparto=info_reparto,
            info_servizio=info_servizio,
            form=form,
            servizio=servizio,
            reparto=reparto,
            info_utente=info_utente,
            info_piatti=info_piatti,
            ordine_id=ordine_id,
            nome=nome,
            cognome=cognome
        )
    else:
        return redirect(url_for('app_cucina.login'))

    
@app_cucina.route('/ordini', methods=['GET', 'POST'])
def ordini():
    """
    Gestisce le operazioni relative agli ordini per il giorno successivo.

    Questa funzione consente di:
    - Recuperare e visualizzare gli ordini esistenti per una data specificata.
    - Creare un nuovo ordine se non esiste già per la data e il servizio specificati.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera i dati necessari per visualizzare gli ordini per la data e il servizio specificati, inclusi i reparti, le schede, i tipi di menu e le informazioni sugli ordini.
    - **POST**: Non implementato esplicitamente nel codice fornito, ma il metodo potrebbe essere utilizzato in futuro per inviare o aggiornare ordini.

    Args:
        None (I parametri di data e servizio sono forniti tramite query string).

    Returns:
        Response:
            - **GET**:
                - Renderizza il template `ordini.html` con i dati recuperati, inclusi:
                    - `year`, `month`, `day`: La data per la quale si visualizzano gli ordini.
                    - `servizio_corrente`: Il servizio corrente selezionato.
                    - `reparti`: I reparti accessibili dall'utente.
                    - `servizio`: Elenco dei servizi disponibili.
                    - `schede`: Elenco delle schede disponibili.
                    - `tipi_menu`: Elenco dei tipi di menu disponibili.
                    - `tipi_alimentazione`: Elenco dei tipi di alimentazione disponibili.
                    - `ordiniSchede`: Ordini già esistenti per la data specificata.
                    - `schede_attive`: Schede attive per i pazienti.
                    - Variabili per il conteggio e i totali degli ordini.
            - **POST**:
                - Status code 302 Found per il redirect alla pagina degli ordini con i dati aggiornati se un nuovo ordine è stato creato con successo.

    Notes:
        - La funzione verifica se l'utente è autenticato; in caso contrario, reindirizza alla pagina di login.
        - Utilizza i servizi per recuperare tutte le informazioni necessarie per il rendering della pagina.
        - Se non esiste un ordine per la data specificata e il servizio, viene creato un nuovo ordine e l'utente viene reindirizzato alla pagina degli ordini.

    Flash Messages:
        - Non sono presenti flash messages nella logica fornita, ma potrebbero essere aggiunti per comunicare il successo della creazione dell'ordine.
    """
    if 'authenticated' in session:
        tomorrow = datetime.now() + timedelta(days=1)
        year = request.args.get('year', tomorrow.year, type=int)
        month = request.args.get('month', tomorrow.month, type=int)
        day = request.args.get('day', tomorrow.day, type=int)
        servizio_corrente = request.args.get('servizio', '1')
        
 
        data = f'{year}-{month}-{day}'

        user_id = session['user_id']
        reparti = get_user_reparti(user_id)


        servizio = service_t_Servizi.get_all_servizi()
        schede = service_t_Schede.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_alimentazione = service_t_TipiAlimentazione.get_all()
        ordiniSchede = service_t_OrdiniSchede.get_all_by_day(year, month, day, servizio_corrente)
        schede_attive = service_t_Schede.get_all_attivi_pazienti()

        schede_count, reparti_totals, schede_totals, total_general = service_t_OrdiniSchede.get_ordini_data(
            year, 
            month, 
            day, 
            servizio_corrente, 
            reparti, 
            schede_attive
        )

        ordine_esistente = service_t_Ordini.existing_Ordine(data, servizio_corrente)

        # Se non esiste, crea un nuovo ordine
        if not ordine_esistente:
            service_t_Ordini.create(data, servizio_corrente)
            return redirect(url_for(
                'app_cucina.ordini',
                servizio_corrente=servizio_corrente, 
                year=year, month=month, 
                day=day
                )
            )
        
        
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        tipi_alimentazione_map = {int(tipo_alimentazione['id']): tipo_alimentazione['descrizione'] for tipo_alimentazione in tipi_alimentazione}
        schede_map = {int(scheda['id']): tipi_menu_map[int(scheda['fkTipoMenu'])] for scheda in schede}
        reparti_map = {int(reparto['id']): reparto['descrizione'] for reparto in reparti}


        return render_template(
            'ordini.html',
            year=year, 
            month=month,
            day=day,
            schede_count=schede_count,
            servizio_corrente=servizio_corrente,
            servizio=servizio,
            schede=schede,
            tipi_menu_map=tipi_menu_map,
            tipi_alimentazione_map=tipi_alimentazione_map,
            reparti=reparti,
            reparti_map=reparti_map,
            schede_map=schede_map,
            ordiniSchede=ordiniSchede,
            schede_count_totali=schede_count,
            reparti_totals=reparti_totals,
            schede_totals=schede_totals,
            total_general=total_general,
            schede_attive=schede_attive,
            ordine_esistente=ordine_esistente
        ) 
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/ordini_dipendenti', methods=['GET', 'POST'])
def ordini_dipendenti():
    """
    Gestisce la visualizzazione e la creazione di ordini per i dipendenti.

    Questa funzione consente di:
    - Visualizzare l'elenco degli ordini dei dipendenti esistenti per un determinato giorno e servizio.
    - Creare un nuovo ordine per il giorno corrente o per un giorno futuro, se non esiste già.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza gli ordini per i dipendenti del giorno specificato.
    - **POST**: Crea un nuovo ordine per il giorno e il servizio selezionati.

    Args:
        Nessuno. Le informazioni sul giorno, il servizio e gli ordini sono gestite attraverso le query string e i dati di sessione.

    Query Parameters:
        year (int, optional): L'anno da visualizzare o su cui creare un ordine (default è l'anno di domani).
        month (int, optional): Il mese da visualizzare o su cui creare un ordine (default è il mese di domani).
        day (int, optional): Il giorno da visualizzare o su cui creare un ordine (default è il giorno di domani).
        servizio (int, optional): Il servizio (ad esempio colazione, pranzo) da visualizzare o su cui creare un ordine (default è '1').

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'ordini_dipendenti.html' con i seguenti dati:
                    - Informazioni sugli ordini esistenti per la data e il servizio selezionati.
                    - Mappa delle schede, tipi di menu, tipi di alimentazione e reparti.
                    - Form per inserire un nuovo ordine.
                    - Dati aggregati sugli ordini, come il conteggio delle schede, i totali per reparti e schede, e il totale generale.
            - **POST**:
                - Se un ordine non esiste già per il giorno e il servizio selezionati, ne viene creato uno nuovo.
                - Reindirizza alla pagina aggiornata degli ordini.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La funzione utilizza vari servizi per recuperare dati come schede, tipi di menu, tipi di alimentazione e reparti.
        - Se non esiste già un ordine per il giorno e il servizio selezionati, ne viene creato uno nuovo e si ricarica la pagina.
        - Il form per gli ordini consente di selezionare e modificare le schede e le quantità di ordini per il servizio scelto.
    """
    if 'authenticated' in session:
        tomorrow = datetime.now() + timedelta(days=1)
        year = request.args.get('year', tomorrow.year, type=int)
        month = request.args.get('month', tomorrow.month, type=int)
        day = request.args.get('day', tomorrow.day, type=int)
        servizio_corrente = request.args.get('servizio', '1')
        
 
        data = f'{year}-{month}-{day}'

        user_id = session['user_id']
        reparti = get_user_reparti(user_id)


        servizio = service_t_Servizi.get_all_servizi()
        schede = service_t_Schede.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_alimentazione = service_t_TipiAlimentazione.get_all()
        ordiniSchede = service_t_OrdiniSchede.get_all_by_day(year, month, day, servizio_corrente)
        schede_attive = service_t_Schede.get_all_personale()

        schede_count, reparti_totals, schede_totals, total_general = service_t_OrdiniSchede.get_ordini_data(
            year, 
            month, 
            day, 
            servizio_corrente, 
            reparti, 
            schede_attive
        )

        ordine_esistente = service_t_Ordini.existing_Ordine(data, servizio_corrente)

        # Se non esiste, crea un nuovo ordine
        if not ordine_esistente:
            service_t_Ordini.create(data, servizio_corrente)
            return redirect(url_for('app_cucina.ordini_dipendenti',servizio_corrente=servizio_corrente, year=year, month=month, day=day))
        

        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        tipi_alimentazione_map = {int(tipo_alimentazione['id']): tipo_alimentazione['descrizione'] for tipo_alimentazione in tipi_alimentazione}
        schede_map = {int(scheda['id']): tipi_menu_map[int(scheda['fkTipoMenu'])] for scheda in schede}
        reparti_map = {int(reparto['id']): reparto['descrizione'] for reparto in reparti}

        form = ordineSchedaForm()


        return render_template(
            'ordini_dipendenti.html',
            year=year,
            month=month,
            day=day,
            schede_count=schede_count,
            servizio_corrente=servizio_corrente,
            servizio=servizio,
            schede=schede,
            tipi_menu_map=tipi_menu_map,
            tipi_alimentazione_map=tipi_alimentazione_map,
            reparti=reparti,
            reparti_map=reparti_map,
            schede_map=schede_map,
            ordiniSchede=ordiniSchede,
            schede_count_totali=schede_count,
            reparti_totals=reparti_totals,
            schede_totals=schede_totals,
            total_general=total_general,
            schede_attive=schede_attive,
            ordine_esistente=ordine_esistente,
            form=form
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/creazione_utenti', methods=['GET', 'POST'])
def creazione_utenti():
    """
    Gestisce la visualizzazione e la creazione di nuovi utenti.

    Questa funzione consente di:
    - Visualizzare l'elenco di tutti gli utenti esistenti.
    - Creare un nuovo utente tramite un form, specificando dati come il nome, cognome, email, tipologia utente, reparto e altre informazioni.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Mostra il modulo per la creazione di un nuovo utente e l'elenco degli utenti esistenti.
    - **POST**: Consente di creare un nuovo utente utilizzando i dati inviati tramite il form.

    Args:
        Nessuno. Le informazioni sugli utenti, i reparti, le tipologie utente e le funzionalità sono gestite attraverso vari servizi.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'creazione_utenti.html' con i seguenti dati:
                    - Elenco degli utenti esistenti.
                    - Form per la creazione di un nuovo utente, con campi pre-popolati per le tipologie di utente, i reparti e le funzionalità.
                    - Mappa delle tipologie utente e reparti, utilizzata per la visualizzazione nel form.
            - **POST**:
                - Se il form è valido e i dati sono corretti:
                    - Crea un nuovo utente nel sistema.
                    - Mostra un messaggio di successo e ricarica la pagina per visualizzare l'utente creato.
                - Se c'è un errore durante la creazione:
                    - Restituisce un messaggio di errore e mantiene il form con gli errori di validazione.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Il form di creazione di un utente include campi per:
            - Username, nome, cognome, email, password.
            - Selezione della tipologia di utente (ad esempio, amministratore o dipendente).
            - Selezione di uno o più reparti.
            - Selezione delle funzionalità personalizzate.
            - Definizione delle date di inizio e fine della validità dell'utente.
        - Se il form viene inviato correttamente, viene chiamato il servizio per creare un nuovo utente.
    """
    if 'authenticated' in session:
        
        # Recupera tutti gli utenti
        utenti = service_t_utenti.get_all()
        # Recupera tutte le tipologie di utente
        tipologieUtente = service_t_tipiUtenti.get_tipiUtenti_all()
        # Recupera tutti i reparti
        reparti = service_t_Reparti.get_all()
        # Recupera tutte le funzionalità
        funzionalita = service_t_funzionalita.get_all_menus()
        # Prepara le scelte per i campi del modulo
        tipologieUtente_map = {int(tipologia['id']): tipologia['nomeTipoUtente'] for tipologia in tipologieUtente}
        reparti_map = {int(reparto['id']): reparto['descrizione'] for reparto in reparti}
        form = UtenteForm()
        form.fkTipoUtente.choices = [(tipologia['id'], tipologia['nomeTipoUtente']) for tipologia in tipologieUtente]
        form.reparti.choices = [(reparto['id'], reparto['descrizione']) for reparto in reparti]
        form.fkFunzCustom.choices = [(funz['id'], funz['titolo']) for funz in funzionalita]
            
        if form.validate_on_submit():
            try:
                # Recupera i dati dal modulo
                username = form.username.data
                nome = form.nome.data
                cognome = form.cognome.data
                fkTipoUtente = form.fkTipoUtente.data
                fkFunzCustom = form.fkFunzCustom.data
                reparti = form.reparti.data
                email = form.email.data
                password = form.password.data
                inizio = form.inizio.data
                fine = form.fine.data


                # Chiamata al servizio per creare l'utente
                service_t_utenti.create_utente(
                    username=username,
                    nome=nome,                        
                    cognome=cognome,
                    fkTipoUtente=fkTipoUtente,
                    fkFunzCustom=fkFunzCustom,
                    reparti=reparti,
                    email=email,
                    password=password,
                    inizio=inizio,
                    fine=fine
                )

                flash('Utente creato con successo!', 'success')
                return redirect(url_for('app_cucina.creazione_utenti'))

            except Exception as e:
                print(f'Errore durante la creazione dell\'utente: {str(e)}')  # Stampa per debug
                flash(f'Errore durante la creazione dell\'utente: {str(e)}', 'error')
            

        return render_template(
            'creazione_utenti.html',
            utenti=utenti,
            tipologieUtente=tipologieUtente,
            reparti=reparti,
            form=form,
            tipologieUtente_map=tipologieUtente_map,
            reparti_map=reparti_map
        )

    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/creazione_utenti/impersonate/<string:public_id>', methods=['POST'])
def impersonate_user(public_id):
    """
    Consente a un amministratore di impersonare un altro utente.

    Questa funzione consente di:
    - Impersonare un utente specifico, permettendo all'amministratore di accedere al sistema come se fosse quell'utente.
    - Aggiorna la sessione con le credenziali dell'utente impersonato.

    La funzione esegue le seguenti operazioni a seconda delle condizioni:
    - Verifica che l'utente corrente sia autenticato e abbia i privilegi di amministratore.
    - Recupera l'utente da impersonare utilizzando il suo `public_id`.
    - Se l'utente viene trovato, la sessione viene svuotata e riempita con le informazioni dell'utente impersonato.
    - Se l'utente non viene trovato, viene restituito un errore e l'utente rimane autenticato come amministratore.

    Args:
        public_id (str): L'ID pubblico dell'utente da impersonare.

    Returns:
        Response:
            - **POST**:
                - Se l'utente è autenticato come amministratore e l'utente da impersonare viene trovato:
                    - La sessione viene aggiornata con le credenziali dell'utente impersonato.
                    - L'utente viene reindirizzato alla homepage con i privilegi del nuovo utente.
                - Se l'utente da impersonare non viene trovato:
                    - Mostra un messaggio di errore e reindirizza l'amministratore alla homepage.
                - Se l'utente corrente non è amministratore:
                    - Mostra un messaggio di errore e reindirizza l'utente alla homepage.

    Notes:
        - Solo gli utenti con `fkTipoUtente` pari a 1 (amministratore) possono eseguire questa operazione.
        - La sessione viene completamente cancellata e ricreata con le informazioni dell'utente impersonato.
        - Se l'utente impersonato ha delle funzionalità personalizzate, queste vengono caricate nella sessione.

    Example:
        POST /creazione_utenti/impersonate/<public_id>

    Security:
        - Se l'utente non è autenticato o non ha i privilegi di amministratore, l'accesso a questa funzionalità viene negato.
    """
    if 'authenticated' in session and session.get('fkTipoUtente') == 1:
        user = service_t_utenti.get_utente_by_public_id(public_id)
        print('user: ' , user)

        if user:
            session.clear()

            user = service_t_utenti.login_da_admin(public_id)  # Call do_login first
            print(user)
            session['authenticated'] = True
            session['user_id'] = public_id
            session['token'] = user['token']
            session['fkTipoUtente'] = user['fkTipoUtente']
            session['username'] = user['username']

            menu_structure = service_t_FunzionalitaUtente.build_menu_structure(user['public_id'])
            session['menu_structure'] = menu_structure
            
            return redirect(url_for('app_cucina.home'))
        else:
            flash('Utente non trovato per l\'impersonificazione.', 'error')
            return redirect(url_for('app_cucina.home'))
    
    flash('Azione non autorizzata.', 'error')
    return redirect(url_for('app_cucina.home'))



@app_cucina.route('/creazione_utenti/<string:public_id>', methods=['GET', 'PUT'])
def modifica_utente(public_id):
    """
    Gestisce la visualizzazione e la modifica dei dati di un utente.

    Questa funzione consente di:
    - Recuperare i dati di un utente specifico in base al suo `public_id`.
    - Aggiornare i dettagli di un utente, come il tipo di utente, i reparti e le date di inizio/fine.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera i dati di un utente specifico e restituisce le informazioni in formato JSON.
    - **PUT**: Aggiorna i dati dell'utente con le informazioni fornite in formato JSON.

    Args:
        public_id (str): L'ID pubblico dell'utente da modificare.

    Returns:
        Response:
            - **GET**:
                - Restituisce un oggetto JSON contenente i dettagli dell'utente, inclusi:
                    - `username`: Il nome utente dell'utente.
                    - `nome`: Il nome dell'utente.
                    - `cognome`: Il cognome dell'utente.
                    - `fkTipoUtente`: Il tipo di utente associato.
                    - `fkFunzCustom`: Funzionalità personalizzate, se presenti.
                    - `inizio`: La data di inizio associata all'utente.
                    - `fine`: La data di fine associata all'utente.
                    - `reparti`: Un elenco dei reparti assegnati all'utente.
                    - `email`: L'indirizzo email dell'utente.
                - Se l'utente non viene trovato, restituisce un codice di stato 404 (Not Found).
            - **PUT**:
                - Aggiorna i dettagli dell'utente in base ai dati forniti nel corpo della richiesta JSON.
                - Se l'aggiornamento ha successo, restituisce un messaggio di conferma con stato 200 (OK).
                - Se ci sono errori nella validazione o durante l'aggiornamento, restituisce un messaggio di errore con stato 400 (Bad Request) o 500 (Internal Server Error).

    Notes:
        - L'utente deve essere autenticato per accedere a questa funzione.
        - Se l'utente non è autenticato, viene restituito un codice di stato 403 (Forbidden).
        - La funzione utilizza il servizio `service_t_utenti` per recuperare e aggiornare i dati dell'utente.

    Example:
        - **GET**: Recupera i dati di un utente:
            GET /creazione_utenti/<public_id>
        - **PUT**: Aggiorna i dati dell'utente:
            PUT /creazione_utenti/<public_id>

    Logs:
        - Registra un messaggio informativo se i dati dell'utente vengono trovati.
        - Registra un avviso se l'utente non viene trovato o se si verifica un errore durante l'aggiornamento.

    Security:
        - L'accesso a questa funzione è limitato agli utenti autenticati.
    """
    if 'authenticated' in session:
        if request.method == 'GET':
            utenti = service_t_utenti.get_utente_by_public_id(public_id)
            print (utenti)
            if utenti:
                logging.info(f"User data found: {utenti}")
                reparti_ids = utenti.get('reparti').split(',') if utenti.get('reparti') else []
                response = {
                    'username': utenti.get('username'),
                    'nome': utenti.get('nome'),   
                    'cognome': utenti.get('cognome'),
                    'fkTipoUtente': utenti.get('fkTipoUtente'),
                    'fkFunzCustom': utenti.get('fkFunzCustom'),
                    'inizio': utenti.get('inizio'),
                    'fine': utenti.get('fine'),
                    'reparti': reparti_ids,      
                    'email': utenti.get('email')
                }
                logging.info(f"Response JSON: {response}")
                return jsonify(response)
            else:
                flash('Utente non trovato.', 'danger')
                logging.warning(f"User with public_id {public_id} not found.")
                return '', 404  # Status code 404 Not Found

        if request.method == 'PUT':
            try:
                json_data = request.get_json()


                if json_data:
                    try:
                        service_t_utenti.update_da_pagina_admin(
                            public_id=public_id,
                            fkTipoUtente=json_data.get('fkTipoUtente'),
                            reparti=json_data.get('reparti'),
                            inizio=json_data.get('inizio'),
                            fine=json_data.get('fine')
                        )
                        return jsonify({'message': 'Reparto aggiornato con successo!'}), 200
                    except Exception as e:
                        print(f"Errore durante l'aggiornamento: {e}")
                        return jsonify({'error': 'Errore durante l\'aggiornamento del reparto'}), 500
                else:
                    print("Errori di validazione del form:", json_data)  # For debugging
                    return jsonify({'error': 'Errore nella validazione dei dati'}), 400
            except Exception as e:
                print(f"Errore nella richiesta: {e}")
                return jsonify({'error': 'Errore nella richiesta'}), 400
    else:
        return jsonify({'error': 'Non autorizzato'}), 403  # Forbidden if not authenticated



@app_cucina.route('/creazione_tipologia_utenti', methods=['GET', 'POST'])
def creazione_tipologia_utenti():
    """
    Gestisce la creazione di nuove tipologie di utente e l'associazione di permessi alle funzionalità.

    Questa funzione consente di:
    - Visualizzare le tipologie di utente esistenti.
    - Visualizzare le funzionalità disponibili e assegnarle con permessi specifici a una nuova tipologia di utente.
    - Creare una nuova tipologia di utente con le funzionalità selezionate e i permessi associati.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza le tipologie di utente esistenti, le funzionalità disponibili e i permessi attuali.
    - **POST**: Crea una nuova tipologia di utente e associa le funzionalità selezionate con i permessi specificati.

    Args:
        Nessuno. I dati necessari per la creazione della tipologia e dei permessi sono ottenuti attraverso i form.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'creazione_tipi_utenti.html' con le seguenti informazioni:
                    - Elenco delle tipologie di utente esistenti.
                    - Elenco delle funzionalità disponibili e la mappa delle funzionalità.
                    - Form per la creazione di una nuova tipologia di utente.
                    - Permessi già associati alle tipologie esistenti.
            - **POST**:
                - Crea una nuova tipologia di utente.
                - Associa le funzionalità selezionate e i relativi permessi al nuovo tipo di utente.
                - Reindirizza nuovamente alla pagina di creazione delle tipologie di utente.

    Query Parameters:
        Nessuno. Le informazioni sono ottenute tramite il form nel corpo della richiesta.

    Notes:
        - La funzione è accessibile solo agli utenti autenticati.
        - I dati sui permessi delle funzionalità vengono recuperati e gestiti tramite i servizi `service_t_tipiUtenti`, 
          `service_t_FunzionalitaUtente`, e `service_t_funzionalita`.
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
    """ 
    if 'authenticated' in session:
        tipologieUtente = service_t_tipiUtenti.get_tipiUtenti_all()
        funzionalita_per_tipologia = {}

        for tipo_utente in tipologieUtente:
            funzionalita_utente = service_t_FunzionalitaUtente.get_funz_utenti_by_user_type(tipo_utente['id'])
            funzionalita_per_tipologia[tipo_utente['id']] = funzionalita_utente

        funzionalita = service_t_funzionalita.get_all_menus()
        print(funzionalita)
        funzionalita_map = {int(funz['id']): funz['titolo'] for funz in funzionalita}
        print(funzionalita_map)
        if request.method == 'POST':
            tipo_utente = request.form.get('fkTipoUtente')
            funzionalita_selezionate = request.form.getlist('funzionalita')
            permessi = {}

            # Recupera i permessi per ogni funzionalità selezionata
            for funz_id in funzionalita_selezionate:
                try:
                    funz_id_int = int(funz_id)
                    permesso_key = f"permesso_{funz_id_int}"
                    permesso_value = request.form.get(permesso_key) == 'true'
                    permessi[funz_id_int] = permesso_value
                except ValueError:
                    print(f"Valore non valido per ID funzionalità: {funz_id}")

            # Crea il nuovo tipo utente e ottieni il suo ID
            nuovo_tipo_utente_id = service_t_tipiUtenti.create(tipo_utente)

            # Associa le funzionalità e i permessi al nuovo tipo utente
            for funz_id, permesso in permessi.items():

                service_t_FunzionalitaUtente.create(nuovo_tipo_utente_id, funz_id, permesso)

            return redirect(url_for('app_cucina.creazione_tipologia_utenti'))

        return render_template(
            'creazione_tipi_utenti.html',
            tipologieUtente=tipologieUtente,
            funzionalita_map=funzionalita_map,
            form=TipoUtenteForm(),
            funzionalita_per_tipologia=funzionalita_per_tipologia
        )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/creazione_tipologia_utenti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_tipo_utente(id):
    """
    Gestisce la visualizzazione, modifica e cancellazione di una tipologia di utente esistente.

    Questa funzione consente di:
    - Visualizzare le informazioni di un tipo di utente specifico e le funzionalità associate.
    - Modificare le informazioni e le funzionalità associate a un tipo di utente.
    - Gestire la cancellazione di una tipologia di utente (attualmente non implementata per motivi di sicurezza).

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza le informazioni di un tipo di utente e delle funzionalità associate.
    - **PUT**: Modifica il tipo di utente e aggiorna le funzionalità e i permessi associati.
    - **DELETE**: Gestisce (simulativamente) la cancellazione del tipo di utente (attualmente non consentita).

    Args:
        id (int): L'ID del tipo di utente da modificare o eliminare.

    Returns:
        Response:
            - **GET**:
                - Restituisce un JSON con i seguenti dati:
                    - `tipo_utente`: Informazioni sul tipo di utente (nome, ID, ecc.).
                    - `funzionalita`: Elenco di tutte le funzionalità disponibili nel sistema con i loro titoli.
                    - `funzionalita_associate`: Funzionalità attualmente associate al tipo di utente.
            - **PUT**:
                - Aggiorna il nome del tipo di utente e le sue funzionalità associate.
                - Restituisce un messaggio di conferma dell'aggiornamento se ha successo.
                - Restituisce un messaggio di errore in caso di fallimento.
            - **DELETE**:
                - Simula la cancellazione del tipo di utente, ma restituisce un messaggio di conferma che l'azione non è consentita.
                - Restituisce un codice di stato `204 No Content` in caso di successo o `400 Bad Request` in caso di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - La cancellazione effettiva dei tipi di utenti non è consentita, ma un messaggio simula l'operazione.
        - La funzione utilizza vari servizi per recuperare e aggiornare i dati dei tipi di utenti e delle funzionalità.
        - Durante la modifica, le funzionalità esistenti vengono eliminate e le nuove selezioni vengono salvate con i relativi permessi.
    """   
    if 'authenticated' in session:
        if request.method == 'GET':
            tipo_utente = service_t_tipiUtenti.get_by_id(id)
            funzionalita_associate = service_t_FunzionalitaUtente.get_funz_utenti_by_user_type(id)
            funzionalita = service_t_funzionalita.get_all_menus()
            funzionalita_map = {int(funz['id']): funz['titolo'] for funz in funzionalita}

            form = TipoUtenteForm(obj=tipo_utente)

            return jsonify({
                'tipo_utente': tipo_utente,
                'funzionalita': funzionalita_map,
                'funzionalita_associate': funzionalita_associate
            })
        
        if request.method == 'PUT':
            tipo_utente = request.form.get('fkTipoUtente')
            if not tipo_utente:
                return jsonify({'Error': 'Nome tipo utente non fornito'}), 400
            
            # Aggiorna il tipo di utente
            try:
                service_t_tipiUtenti.update(id=id, nomeTipoUtente=tipo_utente)
                
                # Elimina le funzionalità esistenti per il tipo utente specificato
                service_t_FunzionalitaUtente.delete_by_tipo_utente(tipo_utente_id=id)

                funzionalita_selezionate = request.form.getlist('funzionalita')
                permessi = {}

                # Recupera i permessi per ogni funzionalità selezionata
                for funz_id in funzionalita_selezionate:
                    try:
                        funz_id_int = int(funz_id)
                        permesso_key = f"permesso_{funz_id_int}"
                        permesso_value = request.form.get(permesso_key) == 'true'
                        permessi[funz_id_int] = permesso_value
                    except ValueError:
                        print(f"Valore non valido per ID funzionalità: {funz_id}")

                # Associa le funzionalità e i permessi al tipo utente
                for funz_id, permesso in permessi.items():
                    service_t_FunzionalitaUtente.create(id, funz_id, permesso)

                return jsonify({'message': 'Tipo utente aggiornato con successo!'}), 200

            except Exception as e:
                print(f"Errore durante l'aggiornamento: {e}")
                return jsonify({'Error': 'Errore durante l\'aggiornamento'}), 500

        if request.method == 'DELETE':
            # Gestione della richiesta DELETE, se necessario
            print(f"Request to delete scheda with ID: {id}")  # Aggiungi questo log
            try:
                # service_t_FunzionalitaUtente.delete_by_tipo_utente(tipo_utente_id=id)
                # service_t_tipiUtenti.delete_tipoUtente(id=id)
                flash('ti piacerebbe! non si possono elimeinare i tipi utenti!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione del tipo utente.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori

    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/qualifiche', methods=['GET', 'POST'])
def qualifiche():
    if 'authenticated' in session:

 
        return render_template('qualifiche.html'
                              
                               )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/impostazioni', methods=['GET', 'POST'])
def impostazioni():
    """
    Gestisce la visualizzazione e la modifica delle impostazioni dell'utente.

    Questa funzione consente di:
    - Visualizzare le impostazioni attuali dell'utente loggato.
    - Cambiare la password dell'utente, se la vecchia password è corretta e la nuova password viene confermata correttamente.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza le impostazioni dell'utente loggato, incluso il tipo di utente associato.
    - **POST**: Verifica la vecchia password, controlla la corrispondenza tra la nuova password e la sua conferma, e aggiorna la password se tutti i controlli sono validi.

    Args:
        Nessuno. I dati dell'utente sono recuperati dalla sessione attiva.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'impostazioni.html' con i seguenti dati:
                    - Informazioni dell'utente loggato, come il nome utente e il tipo utente.
                    - Mappa dei tipi di utente disponibili.
                    - Form per il cambio password.
            - **POST**:
                - Se la vecchia password è corretta e la nuova password viene confermata, la password viene aggiornata e un messaggio di successo viene mostrato.
                - In caso di errori, vengono mostrati messaggi di errore specifici (es. vecchia password errata, nuova password non confermata correttamente).

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Il form per il cambio password include i seguenti campi: username (non modificabile), vecchia password, nuova password e conferma della nuova password.
        - Il controllo sulla validità della vecchia password viene effettuato tramite il servizio `service_t_utenti`.
        - La nuova password viene aggiornata solo se tutti i controlli sono superati con successo.
    """
    if 'authenticated' in session:
        user = service_t_utenti.get_utente_by_public_id(session['user_id'])
        tipi_utenti = service_t_tipiUtenti.get_tipiUtenti_all()

        tipi_utenti_map = {int(tipo_utente['id']): tipo_utente['nomeTipoUtente'] for tipo_utente in tipi_utenti}

        form = CambioPasswordForm()
        form_email = CambioEmailForm()

        if form_email.validate_on_submit():
            # Verifica la vecchia password
            password_ok = service_t_utenti.check_password(
                username=session['username'],  # Usa l'username dell'utente loggato
                password=form_email.password.data
            )

            if password_ok:
                email = form_email.email.data
                email_conferma = form_email.email_conferma.data  # Campo di conferma dell'email

                # Controlla se la nuova email e la conferma corrispondono
                if email == email_conferma:
                    # Aggiorna l'email nel database
                    service_t_utenti.update_utente_email(session['user_id'], email)
                    flash('E-mail cambiata con successo!', 'success')
                    return redirect(url_for('app_cucina.impostazioni'))  # Reindirizza alla pagina delle impostazioni
                else:
                    flash('La nuova e-mail e la conferma non corrispondono.', 'error')
            else:
                flash('Password errata. Riprova.', 'error')
                    

        if form.validate_on_submit():
            # Verifica la vecchia password
            password_ok = service_t_utenti.check_password(
                form.username.data,  # Usa l'username dell'utente loggato
                form.password.data
            )

            if password_ok:
                # Verifica se la nuova password e la conferma sono uguali
                if form.nuova_password.data == form.ripeti_nuova_password.data:
                    # Aggiorna la password dell'utente
                    service_t_utenti.update_utente_password_by_username(
                        form.username.data,  # Usa l'username dell'utente loggato
                        form.nuova_password.data
                    )
                    flash('Password cambiata con successo!', 'success')
                else:
                    flash('La nuova password e la conferma non corrispondono.', 'error')
            else:
                flash('La vecchia password è errata.', 'error')

        return render_template(
            'impostazioni.html',
            user=user,
            tipi_utenti_map=tipi_utenti_map,
            form=form,
            form_email=form_email
        )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/contatti', methods=['GET', 'POST'])
def contatti():
    """
    Gestisce l'invio di segnalazioni e messaggi di contatto da parte degli utenti.

    Questa funzione consente di:
    - Visualizzare un modulo di contatto per inviare segnalazioni o richieste di assistenza.
    - Inviare un messaggio di contatto all'amministratore del sistema.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **GET**: Recupera e visualizza il modulo di contatto precompilato con le informazioni dell'utente loggato.
    - **POST**: Valida i dati del modulo e invia un messaggio di contatto all'indirizzo email specificato, utilizzando i dati forniti dall'utente.

    Args:
        Nessuno. Le informazioni dell'utente sono recuperate dalla sessione attiva.

    Returns:
        Response:
            - **GET**:
                - Mostra la pagina 'contatti.html' con i seguenti dati:
                    - Informazioni dell'utente loggato, come nome, cognome e email.
                    - Form per l'invio di segnalazioni.
            - **POST**:
                - Se il modulo è validato con successo, invia un messaggio all'amministratore e mostra un messaggio di conferma all'utente.
                - In caso di errore durante l'invio, mostra un messaggio di errore.

    Notes:
        - Se l'utente non è autenticato, viene reindirizzato alla pagina di login.
        - Il form di contatto include i seguenti campi: oggetto e messaggio.
        - Il messaggio inviato include il nome, l'email e il contenuto del messaggio dell'utente.
        - Eventuali errori nell'invio del messaggio vengono registrati per facilitare il debug.
    """ 
    if 'authenticated' in session:
        user = service_t_utenti.get_utente_by_public_id(session['user_id'])
        nome = user['nome']  # Accesso ai valori del dizionario
        cognome = user['cognome']  # Accesso ai valori del dizionario
        email = user['email']
        
        form = ContattiForm()

        if form.validate_on_submit():
            oggetto = form.oggetto.data
            messaggio = form.messaggio.data

            # Creiamo il messaggio da inviare
            msg = Message(f"Segnalazione da {cognome} {nome}: {oggetto}",
                          sender=email,  # Usa l'indirizzo dell'utente come mittente
                          recipients=['ptest2420@gmail.com'])  # L'indirizzo a cui inviare le segnalazioni
            msg.body = f"Nome: {nome}\nEmail: {email}\n\nMessaggio:\n{messaggio}"
            msg.reply_to = email  # Imposta l'indirizzo di risposta
            
            try:
                mail.send(msg)
                flash('Il tuo messaggio è stato inviato con successo!', 'success')
            except Exception as e:
                flash('C\'è stato un errore nell\'invio del messaggio. Riprova più tardi.', 'danger')
                print(str(e))  # Log dell'errore per debug

        return render_template('contatti.html', user=user, form=form)
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/do_logout', methods=['POST'])
def do_logout():
    """
    Gestisce il processo di logout dell'utente.

    Questa funzione consente di:
    - Disconnettere l'utente dalla sessione attiva.
    - Pulire i dati della sessione per garantire la sicurezza.

    La funzione esegue le seguenti operazioni a seconda del metodo HTTP della richiesta:
    - **POST**: Valida la richiesta di logout e, se valida, esegue la disconnessione dell'utente.

    Args:
        Nessuno. L'autenticazione dell'utente è gestita attraverso la sessione.

    Returns:
        Response:
            - **POST**:
                - Se la richiesta è valida e l'utente è autenticato, l'utente viene disconnesso e viene effettuato un reindirizzamento alla pagina di login.
                - In caso contrario, l'utente viene comunque reindirizzato alla pagina di login.

    Notes:
        - Se l'utente non è autenticato, viene comunque reindirizzato alla pagina di login.
        - La funzione utilizza un modulo di logout per gestire la richiesta, anche se non utilizza il CSRF.
        - La sessione viene pulita completamente per garantire la sicurezza dopo il logout.
    """
    

    if 'authenticated' in session:

        form = LogoutFormNoCSRF()
        if form.validate_on_submit():
            service_t_utenti.do_logout_nuovo(session['user_id'])
            session.clear()

            return redirect(url_for('app_cucina.login'))
        
    return redirect(url_for('app_cucina.login'))




@app_cucina.route('/richiesta_recupero_password', methods=['POST'])
@csrf.exempt  
def richiesta_recupero_password():
    if request.method == 'POST':
        # Ottieni l'email direttamente dalla richiesta
        email = request.form.get('email')  # Usa 'get' per evitare errori se 'email' non esiste
        print("Email submitted: ", email)  # Stampa l'email inviata

        # Verifica se l'utente esiste tramite email
        utente = service_t_utenti.exists_utente_by_email(email)

        if utente:
            # Genera il token per il reset della password
            token = service_t_utenti.generate_reset_password_token(email)
            print("Generated token: ", token)  # Stampa il token generato

            # Crea il messaggio di reset della password
            msg = Message(
                subject="Richiesta di reimpostazione della password",
                sender='ptest2420@gmail.com',  # Usa il sender configurato
                recipients=[email],  # Invia all'email dell'utente
                
            )

            # Crea il link di reset password
            reset_url = url_for('app_cucina.reset_password', token=token, _external=True)
            print("Reset URL: ", reset_url)  # Stampa l'URL di reset

            # Corpo del messaggio email
            msg.body = f"Ciao {utente.nome},\n\n" \
                       f"Hai richiesto di reimpostare la tua password. Clicca sul seguente link per procedere:\n" \
                       f"{reset_url}\n\n" \
                       "Se non hai richiesto questa azione, ignora questa email.\n\n" \
                       "Grazie,\nIl Team"

            try:
                # Invia l'email
                mail.send(msg)
                flash('Un\'email con le istruzioni per il reset della password è stata inviata!', 'success')
            except Exception as e:
                flash('C\'è stato un errore durante l\'invio dell\'email. Riprova più tardi.', 'danger')
                print("Error sending email: ", e)  # Stampa il messaggio di errore

        else:
            # Anche se l'utente non esiste, mostriamo comunque un messaggio di conferma
            flash('l\'email inserita non è corretta .', 'info')

        print("Redirecting to login page...")
        return redirect(url_for('app_cucina.login'))  # Assicurati di indirizzare all'endpoint corretto

    # Se non viene fatto un POST, gestisci il fallback (opzionale)
    flash('Si è verificato un errore nel recupero della password. Riprova.', 'danger')
    print("Form validation failed, redirecting to login page...")
    
    # Reindirizza l'utente alla pagina di login
    return redirect(url_for('app_cucina.login'))


@app_cucina.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = PasswordResetForm()

    try:
        # Verifica la validità del token
        utente = service_t_utenti.get_utente_by_token_valid(token)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('app_cucina.login'))
    
    if form.validate_on_submit():
        # Processa la nuova password
        new_password = form.nuova_password.data
        service_t_utenti.update_utente_password(utente.public_id, new_password)

        flash('La tua password è stata reimpostata con successo!', 'success')
        return redirect(url_for('app_cucina.login'))

    return render_template('reset_password.html', form=form, token=token)

  

#pagina che riporta gli errori
@app_cucina.route('/report_error', methods=['POST'])
def report_error():
    return redirect(url_for('app_cucina.index'))  # Redirect dopo aver inviato il feedback


#chiamata per la pagina degli errori con il tipo di errore
@app_cucina.errorhandler(Exception)
def handle_exception(error):
    # Puoi anche loggare l'errore qui se necessario
    return render_template('error.html', error=str(error))


# Register the blueprint
app.register_blueprint(app_cucina, url_prefix='/app_cucina')

if __name__ == '__main__':
    app.run(debug=True)


