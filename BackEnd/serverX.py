

#from Classi.initialize_db.initialize_db import initialize_database
# Inizializzare il database
#initialize_database()

# Importare i controller
from datetime import datetime, date

import calendar
from functools import wraps
import pprint
import logging

from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti
 

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
from flask import Flask, jsonify, Blueprint, request, session, render_template, redirect, url_for, flash
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
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseForm.form import AlimentiForm, PreparazioniForm, AlimentoForm, PiattiForm, MenuForm, LoginFormNoCSRF, LogoutFormNoCSRF, schedaForm, ordineSchedaForm, schedaPiattiForm, UtenteForm, CloneMenuForm, TipoUtenteForm 
# Initialize the app and configuration
import Reletionships

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['WTF_CSRF_ENABLED'] = True

csrf = CSRFProtect(app)

# Initialize JWT and CORS
jwt = JWTManager(app)
CORS(app)

# Initialize services
service_t_utenti = Service_t_utenti()
service_t_Reparti = Service_t_Reparti()
service_t_Servizi = Service_t_Servizi()
service_t_Alimenti = Service_t_Alimenti()
service_t_tipologiaalimenti = Service_t_tipologiaalimenti()
service_t_Allergeni = Service_t_Allergeni()
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

# Background job for removing expired tokens
def remove_expired_tokens():
    service_t_utenti.expiredTokens()

# Configura lo scheduler per rimuovere i token scaduti ogni minuto
scheduler = BackgroundScheduler()
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

# Decorator per proteggere le rotte
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('authenticated') is False:
            return redirect(url_for('app_cucina.login'))
        return f(*args, **kwargs)
    return decorated_function

#trova il nome utente
def get_username():
    user_id = session.get('user_id')
    user = service_t_utenti.get_utente_by_id(user_id)
    
    return user['username']

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
#funzione per clonare il menu


def clona_menu(menu_id, clone_date, utente_inserimento):
    try:
        def get_menu_data(menu_id):
            assoc_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_id)
            menu = service_t_MenuServizi.get_by_id(menu_id)
            tipo_menu = service_t_Menu.get_by_id(menu['fkMenu'])
            return assoc_piatti, menu, tipo_menu

        assoc_piatti, menu_da_clonare, tipo_menu_da_clonare = get_menu_data(menu_id)

        menu_by_data = service_t_Menu.get_by_data(clone_date, tipo_menu_da_clonare['fkTipoMenu'])

        if menu_by_data is None:
            new_menu_id = service_t_Menu.create(clone_date, tipo_menu_da_clonare['fkTipoMenu'], utenteInserimento=utente_inserimento)
            menu_by_data = service_t_Menu.get_by_id(new_menu_id)

        if not isinstance(menu_by_data, dict):
            raise ValueError("Errore: menu_by_data dovrebbe essere un dizionario")

        menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(menu_by_data['id'], menu_da_clonare['fkServizio'])

        if menu_servizio is None:
            menu_servizio_id = service_t_MenuServizi.create(menu_by_data['id'], menu_da_clonare['fkServizio'], utenteInserimento=utente_inserimento)
            menu_servizio = service_t_MenuServizi.get_by_id(menu_servizio_id)
            if not isinstance(menu_servizio, dict):
                raise ValueError("Errore: menu_servizio dovrebbe essere un dizionario")

        else:
            if not isinstance(menu_servizio, dict):
                raise ValueError("Errore: menu_servizio dovrebbe essere un dizionario")

        # Log dei dati per debugging
        print(f"Menu da clonare: {menu_da_clonare}")
        print(f"Nuovo menu: {menu_by_data}")
        print(f"Servizio associato: {menu_servizio}")

        # Cancella le associazioni esistenti
        service_t_MenuServiziAssociazione.delete_per_menu(menu_servizio['id'], utenteCancellazione=utente_inserimento)

        for associazione in assoc_piatti:
            print(f"Creando associazione: {associazione}")
            service_t_MenuServiziAssociazione.create(menu_servizio['id'], associazione['id'], utenteInserimento=utente_inserimento)

        flash('Menu clonato con successo!', 'success')
        return True

    except ValueError as ve:
        flash(f"Errore di validazione: {str(ve)}", 'error')
        print(f"Errore di validazione: {str(ve)}")
        return False

    except Exception as e:
        flash(f"Errore durante la clonazione del menu: {str(e)}", 'error')
        print(f"Errore durante la clonazione del menu: {str(e)}")
        return False

#filtra i reparti in base ai permessi degli utenti
def get_reparti_utente():
    user_id = session.get('user_id')
    user = service_t_utenti.get_reparti_list(user_id)
    
    # Se 'reparti' è None, restituisce una lista vuota
    return user.get('reparti', []) if user else []


@app_cucina.before_request
def check_token_and_permissions():
    exempt_routes = ['app_cucina.login', 'app_cucina.index' ,'app_cucina.do_logout']

    # Se la rotta corrente è esente, salta il controllo del token e dei permessi
    if request.endpoint in exempt_routes:
        return

    # Verifica se l'utente è autenticato
    if 'authenticated' not in session or not session.get('authenticated'):
        return redirect(url_for('app_cucina.login'))

    # Verifica la validità del token JWT
    try:
        user_id = session.get('user_id')
        if not user_id or not service_t_utenti.is_token_valid(user_id, session.get('token')):
            session.clear()  # Cancella la sessione se il token non è valido
            return redirect(url_for('app_cucina.login'))
    except Exception as e:
        logging.error(f"Error verifying token for user_id {user_id}: {str(e)}")
        session.clear()
        return redirect(url_for('app_cucina.login'))

    # Verifica i permessi di accesso alla rotta corrente
    try:
        user_type_id = session.get('fkTipoUtente')
        page_link = get_page_name_from_path(request.path)

        # Chiamata al servizio per controllare i permessi
        access_granted, message = service_t_funzionalita.can_access(user_type_id=user_type_id, page_link=page_link)
        
        if not access_granted:
            logging.warning(f"Access denied for user_id {user_id} to {page_link}: {message}")
            return redirect(url_for('app_cucina.index'))  # Rotta per accesso negato
        
    except Exception as e:
        logging.error(f"Error checking permissions for user_id {user_id}: {str(e)}")
        return redirect(url_for('app_cucina.index'))


@app_cucina.before_request
def check_csrf():
    exempt_routes = ['app_cucina.login', 'app_cucina.index','app_cucina.do_logout' ]
    if request.endpoint not in exempt_routes:
        csrf.protect()


#login fattio con il form 
@app_cucina.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormNoCSRF()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            user = service_t_utenti.do_login(username, password)
            if user:
                session['authenticated'] = True
                session['user_id'] = user['id']
                session['token'] = user['token']
                session['fkTipoUtente'] = user['fkTipoUtente']
                
                
                
                menu_structure = service_t_FunzionalitaUtente.build_menu_structure(user['id'])
                session['menu_structure'] = menu_structure
                
                return redirect(url_for('app_cucina.index'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('loginx.html', form=form)
        
        except Exception as e:
            print(f"Error during login: {e}")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('loginx.html', form=form)
    
    return render_template('loginx.html', form=form)  # GET request




@app.context_processor
def inject_user_data():
    menu_structure = session.get('menu_structure', [])
    user_id = session.get('user_id')
    user_type = session.get('fkTipoUtente')
    token = session.get('token')

    # Recupera le informazioni dell'utente se disponibile
    user = service_t_utenti.get_utente_by_id(user_id) if user_id else None
    username = user['username'] if user else "Utente"

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

    # Stampa i permessi di tutte le pagine per l'utente corrente (per debug)


    # Ritorna i dati che devono essere accessibili nei template
    return dict(
        menu_structure=menu_structure,
        username=username,
        token=token,
        user_type=user_type,
        form=LogoutFormNoCSRF(),
        current_page_link=request.path,
        page_permissions=page_permissions  # Aggiungi i permessi delle pagine
    )








@app_cucina.route('/index')
def index():
    if 'authenticated' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('app_cucina.login'))

@app_cucina.route('/alimenti', methods=['GET', 'POST'])
@login_required
def alimenti():
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


@app_cucina.route('/alimenti/<int:id>', methods=['DELETE'])
def elimina_alimento(id):
    if 'authenticated' in session:

        print(f"Request to delete Alimento with ID: {id}")  # Aggiungi questo log
        try:
            service_t_Alimenti.delete(id=id)
            flash('Alimento eliminata con successo!', 'success')
            return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
        except Exception as e:
            print(f"Error deleting scheda: {e}")  # Log per l'errore
            flash('Errore durante l\'eliminazione dell\'Alimento', 'danger')
            return '', 400  # Status code 400 Bad Request per errori
       
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('preparazioni/get_tipi_piatti/<int:fkTipoPreparazione>', methods=['GET'])
def get_by_fkTipoPreparazione(fkTipoPreparazione):
    piatti = service_t_Piatti.get_tipipiatti_da_tipoPreparazione(fkTipoPreparazione)
    tutti_i_piatti = service_t_Piatti.get_all()
    return jsonify(piatti if piatti else tutti_i_piatti)

@app_cucina.route('/get_piatti/<tipo_piatto>', methods=['GET'])
def get_piatti_fktipo_piatto(tipo_piatto): 
    piatti_filtarti_menu = service_t_Piatti.get_by_fkTipoPiatto(tipo_piatto)
    return jsonify(piatti_filtarti_menu)


@app_cucina.route('/get_preparazioni/<tipo_piatto>', methods=['GET'])
def get_preparazioni_e_associazione(tipo_piatto): 
    preparazione = service_t_AssociazionePiattiPreparazionie.get_preparazione_by_piatto(tipo_piatto)
    return jsonify(preparazione)



@app_cucina.route('/preparazioni', methods=['GET', 'POST'])
def preparazioni():
    #FACCIAMO TUTTE LE GET CHE CI SEERVONO
    preparazioni = service_t_preparazioni.get_all_preparazioni()
    tipiPreparazioni = service_t_tipipreparazioni.get_all_tipipreparazioni()
    preparazioniContenuti = service_t_preparazionicontenuti.get_all_preparazioni_contenuti()
    piatti = service_t_Piatti.get_all()
    alimenti = service_t_Alimenti.get_all()  # Assuming this method returns a list of alimenti
    tipi_quantita = service_t_tipoquantita.get_all_tipoquantita()  # Assuming this returns a list
    associazione = service_t_AssociazionePiattiPreparazionie.get_all()



    #ISTANZIAMO LE FORM PER COSTRUIRE I FORM NEL HTML
    piattiform = PiattiForm()
    form = PreparazioniForm()
    alimform = AlimentoForm()

    #REIMPIAMO LE POSSIBILI SCELTE DELLE FORM
    form.fkTipoPreparazione.choices = [
        (tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni
    ]

    alimform.fkAlimento.choices = [
        (alimento['id'], alimento['alimento']) for alimento in alimenti
    ]

    alimform.fkTipoQuantita.choices = [
        (tipo_quantita['id'], tipo_quantita['tipo']) for tipo_quantita in tipi_quantita
    ]

    TipoPreparazione_map = {int(tipoPreparazione['id']): tipoPreparazione['descrizione'] for tipoPreparazione in tipiPreparazioni}
    alimento_map = {int(alimento['id']): alimento['alimento'] for alimento in alimenti}
    tipo_map = {int(tipo_quantita['id']): tipo_quantita['tipo'] for tipo_quantita in tipi_quantita}
    if 'authenticated' in session:
        if form.validate_on_submit():
            # Handling the image upload
            if form.immagine.data:
                image_filename = secure_filename(form.immagine.data.filename)
                form.immagine.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            else:
                image_filename = None

            utente_inserimento = get_username()
            fk_piatto = request.form.get('titolo')


            # Create the preparation record and get its ID
            new_preparazione_id = service_t_preparazioni.create_preparazione(
                
                fkTipoPreparazione=form.fkTipoPreparazione.data, 
                descrizione=form.descrizione.data, 
                isEstivo=form.isEstivo.data, 
                isInvernale=form.isInvernale.data,  
                inizio=form.inizio.data if form.inizio.data else None, 
                fine=form.fine.data if form.fine.data else None,  
                utenteInserimento=utente_inserimento, 
                immagine=image_filename
            )



            service_t_AssociazionePiattiPreparazionie.create(
                fkPiatto=fk_piatto, 
                fkPreparazione = new_preparazione_id,
                utenteInserimento = utente_inserimento
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
                        utenteInserimento=utente_inserimento
                    )
                    print(f"Ingredient saved: {ingredient}")
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
            tipo_map=tipo_map

        )
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('app_cucina.login'))



        
@app_cucina.route('/preparazioni/<int:id_preparazione>', methods=['GET', 'POST', 'DELETE'])
def preparazione_dettagli(id_preparazione):
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
            
            form = PreparazioniForm(obj=preparazione)
            alimform = AlimentoForm(obj=preparazione)

            # Riempie le possibili scelte dei form
            form.fkTipoPreparazione.choices = [
                (tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni
            ]

            alimform.fkAlimento.choices = [
                (alimento['id'], alimento['alimento']) for alimento in alimenti
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
                'ingredienti': [
                    {
                        'fkAlimento': ingrediente.get('fkAlimento'),
                        'quantita': ingrediente.get('quantita'),
                        'fkTipoQuantita': ingrediente.get('fkTipoQuantita'),
                        'note': ingrediente.get('note')
                    } for ingrediente in alimentiPerPrep
                ],
                'scelte': {
                    'tipiPreparazioni': [(tipoPreparazione['id'], tipoPreparazione['descrizione']) for tipoPreparazione in tipiPreparazioni],
                    'alimenti': [(alimento['id'], alimento['alimento']) for alimento in alimenti],
                    'tipiQuantita': [(tipo_quantita['id'], tipo_quantita['tipo']) for tipo_quantita in tipi_quantita]
                }
            }
            
        
            return jsonify(data)

        if request.method == 'POST':
            # Logica per gestire il POST
            pass

        if request.method == 'DELETE':
            print(f"Request to delete preparazione with ID: {id_preparazione}")  # Log per la richiesta di cancellazione
            try:
                service_t_AssociazionePiattiPreparazionie.delete_associazione(fkPreparazione=id_preparazione, utenteCancellazione=get_username())
                service_t_preparazionicontenuti.delete_preparazioni_contenuti(fkPreparazione=id_preparazione, utenteCancellazione=get_username())
                service_t_preparazioni.delete_preparazione(id=id_preparazione, utenteCancellazione=get_username())
                
                flash('Preparazione eliminata con successo!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione della preparazione.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori

    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/piatti', methods=['GET', 'POST'])
def piatti():
    # Ottenere tutti i piatti e le tipologie di piatti dal servizio
    piatti = service_t_Piatti.get_all()
    tipologia_piatti = service_t_TipiPiatti.get_all()

    # Mappare le tipologie di piatti per l'uso nel template
    TipoPiatto_map = {int(tipoPiatto['id']): tipoPiatto['descrizione'] for tipoPiatto in tipologia_piatti}

    # Creare un'istanza del form per l'aggiunta di piatti
    form = PiattiForm()

    # Popolare le scelte per il campo fkTipoPiatto nel form
    form.fkTipoPiatto.choices = [(tipoPiatto['id'], tipoPiatto['descrizione']) for tipoPiatto in tipologia_piatti]

    # Verificare se l'utente è autenticato
    if 'authenticated' in session:
        # Se il form è stato inviato e è valido, processa i dati del form
        if form.validate_on_submit():
           
            utente_inserimento = get_username()
           
            try:
                service_t_Piatti.create(
                    fkTipoPiatto=form.fkTipoPiatto.data, 
                    codice=form.codice.data, 
                    titolo=form.titolo.data,
                    descrizione=form.descrizione.data, 
                    inMenu=form.inMenu.data, 
                    ordinatore=form.ordinatore.data, 
                    utenteInserimento=utente_inserimento
                )
                app.logger.debug("Piatto creato con successo nel database.")
            except Exception as e:
                app.logger.error(f"Errore durante la creazione del piatto: {str(e)}")
                return {'Error': str(e)}, 500

            # Se il salvataggio nel database ha successo, aggiorna la lista dei piatti
            piatti = service_t_Piatti.get_all()

            return redirect(url_for('app_cucina.piatti'))
    
    # Se il form non è stato inviato o non è valido, mostra il template con il form vuoto o con errori
        return render_template('piatti.html',
                           piatti=piatti,
                           tipologia_piatti=tipologia_piatti,
                           TipoPiatto_map=TipoPiatto_map,
                           form=form)
    
    # Se l'utente non è autenticato, reindirizzalo alla pagina di login
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/piatti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_piatti(id):
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
            
            try:
                service_t_Piatti.update(
                    id=id,
                    fkTipoPiatto=form.fkTipoPiatto.data, 
                    codice=form.codice.data, 
                    titolo=form.titolo.data,
                    descrizione=form.descrizione.data, 
                    inMenu=form.inMenu.data, 
                    ordinatore=form.ordinatore.data, 
                    utenteInserimento=get_username()
                )
                app.logger.debug("Piatto creato con successo nel database.")
            except Exception as e:
                app.logger.error(f"Errore durante la creazione del piatto: {str(e)}")
                return {'Error': str(e)}, 500


        if request.method == 'DELETE':
            try:
                service_t_Piatti.delete(id, utenteCancellazione=get_username())
                flash('Piatto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content
            
            except Exception as e:
                print(f"Error deleting dish: {e}")
                flash('Errore durante l\'eliminazione del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request

    else:
        return redirect(url_for('app_cucina.login'))












@app_cucina.route('/tipologia_piatti')
def tipologia_piatti():
    tipologia_piatti = service_t_TipiPiatti.get_all()
    if 'authenticated' in session:
        return render_template('tipologia_piatti.html',tipologia_piatti=tipologia_piatti)
    else:
        return redirect(url_for('app_cucina.login'))
   
    

@app_cucina.route('/reparti')
def reparti():
    reparti = service_t_Reparti.get_all()
    if 'authenticated' in session:
        return render_template('reparti.html',reparti=reparti)
    else:
        return redirect(url_for('app_cucina.login'))

@app_cucina.route('/servizi')
def servizi():
    servizi = service_t_Servizi.get_all_servizi()
    if 'authenticated' in session:
        return render_template('servizi.html',servizi=servizi)
    else:
        return redirect(url_for('app_cucina.login'))

@app_cucina.route('/tipologia_menu')
def tipologia_menu():
    tipologie_menu = service_t_TipiMenu.get_all()
    if 'authenticated' in session:
        return render_template('tipologia_menu.html', tipologie_menu=tipologie_menu)
    else:
        return redirect(url_for('app_cucina.login'))
    
    
@app_cucina.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'authenticated' in session:
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
        piatti = service_t_Piatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()
        servizi = service_t_Servizi.get_all_servizi()
        
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
            print('Dati del form POST:', request.form)  # Log dei dati del form
            if clona_mese.validate_on_submit():
                try:
                    # Recupera la data di clonazione e il numero di giorni
                    clone_date_str = form.clone_date.data.strftime('%Y-%m-%d')
                    clone_date = datetime.strptime(clone_date_str, '%Y-%m-%d')
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))
                    utente_inserimento = get_username()

                    # Recupera gli ID dei menu dal form
                    menu_ids = request.form.get('menu_ids').split(',')
                    print(f"Menu IDs: {menu_ids}")

                    # Recupera i servizi associati ai menu
                    menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(menu_ids)
                    print(f"Menu Services: {menu_servizi}")

                    for index, menu_id_str in enumerate(menu_ids):
                        menu_id = int(menu_id_str)  # Converti menu_id in intero
                        giorno_clonazione = clone_date + timedelta(days=index)
                        print(f"Clonazione del menu ID {menu_id} per il giorno {giorno_clonazione.strftime('%Y-%m-%d')}")

                        # Trova i servizi associati a questo menu
                        servizi_per_menu = [servizio for servizio in menu_servizi if servizio['fkMenu'] == menu_id]
                        print(f"Servizi per il menu ID {menu_id}: {servizi_per_menu}")

                        if not servizi_per_menu:
                            print(f"Nessun servizio trovato per il menu ID {menu_id}")

                        for servizio in servizi_per_menu:
                            print(f"Clonazione del servizio ID {servizio['id']} per il giorno {giorno_clonazione.strftime('%Y-%m-%d')}")
                            clona_menu(servizio['id'], giorno_clonazione.strftime('%Y-%m-%d'), utente_inserimento)

                    flash('Mese clonato con successo!', 'success')
                    return redirect(next_url)

                except Exception as e:
                    flash(f"Errore durante la clonazione del mese: {str(e)}", 'error')
                    print(f"Errore: {str(e)}")



            
            
            if form.validate_on_submit():
                try:
                    menu_id = request.form['menu_id']
                    clone_date = form.clone_date.data.strftime('%Y-%m-%d')
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))
                    utente_inserimento = get_username()

                    # Chiama la funzione per clonare il menu
                    if clona_menu(menu_id, clone_date, utente_inserimento):
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
                    piatti=piatti,
                    preparazioni=preparazioni,
                    datetime=datetime,
                    calendar=calendar,
                    week_numbers=week_numbers,  # Passa i numeri delle settimane al template
                    form=form,
                    clona_mese=clona_mese,
                    menu_ids=menu_ids
                    
                )
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/menu/<int:id_menu>', methods=['DELETE'])
def cose_menu(id_menu):
    if 'authenticated' in session:

        if request.method == 'DELETE':
            # Gestione dell'Eliminazione del Menu
            print(f"Request to delete menu with ID: {id_menu}")
            try:
                menu = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(id_menu)
                print(menu)
                service_t_MenuServiziAssociazione.delete_per_menu(id_menu, utenteCancellazione=get_username())
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
            utente = get_username()
            
            # Raccogli le associazioni selezionate dall'utente
            piatto_e_prep = []
            for piatto_id in request.form.getlist('piatti'):
                preparazioni_ids = request.form.getlist(f'preparazioni-{piatto_id}')
                for preparazione_id in preparazioni_ids:
                    piatto_e_prep.append({
                        'fkPiatto': piatto_id,
                        'fkPreparazione': preparazione_id
                    })
            print(piatto_e_prep)

            associazioni_id = []
            for assoc in piatto_e_prep:
                result = service_t_AssociazionePiattiPreparazionie.get_id_by_preparazione_e_piatto(assoc['fkPiatto'], assoc['fkPreparazione'])
                if 'Error' in result:
                    app.logger.error(f"Errore durante il recupero dell'associazione: {result['Error']}")
                    return {'Error': result['Error']}, 500
                associazioni_id.append(result['id'])
            print(associazioni_id)
            # Elenco delle nuove associazioni da inserire
            try:
                # Elimina le associazioni esistenti
                if associazioni:
                    service_t_MenuServiziAssociazione.delete_per_menu(fkMenuServizio=id_menu, utenteCancellazione=utente)
               
                # Crea le nuove associazioni
                for assoc_id in associazioni_id:
                    response = service_t_MenuServiziAssociazione.create(
                        fkMenuServizio=id_menu,
                        fkAssociazione=assoc_id,
                        utenteInserimento=utente
                    )

                    print(response)
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
        return render_template('dettaglio_menu.html', 
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
                utenteInserimento=get_username()
            )

            flash('Scheda aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.schede'))

        return render_template('schede.html',
                               schede=schede,
                               tipi_menu_map=tipi_menu_map,
                               tipi_alimentazione_map=tipi_alimentazione_map,
                               form=form,
                               )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/schede/<int:id>', methods=['GET', 'POST', 'DELETE'])
def modifica_scheda(id):
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
                utenteInserimento=get_username()
            )

            flash('Scheda aggiornata con successo!', 'success')
            return redirect(url_for('app_cucina.schede'))
        

    if request.method == 'DELETE':
        print(f"Request to delete scheda with ID: {id}")  # Aggiungi questo log
        try:
            service_t_Schede.delete(id=id, utenteCancellazione=get_username())
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
    if 'authenticated' in session:
        
        servizio_corrente = request.args.get('servizio', '1')
        print(servizio_corrente)
        
        
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
                    utenteInserimento=get_username()
                )
                
                flash('Scheda aggiunta con successo!', 'success')
                return redirect(url_for('app_cucina.schede_piatti', id=id, servizio=servizio_corrente))
            except Exception as e:
                flash(f'Errore durante l\'aggiunta della scheda: {str(e)}', 'danger')
                # Potresti anche loggare l'eccezione se necessario
                app.logger.error(f'Errore: {str(e)}')

        return render_template('schede_piatti.html',
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
                service_t_SchedePiatti.delete_piatto_singolo(id=id_piatto_scheda, utenteCancellazione=get_username())

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
                    utenteInserimento=get_username()
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
                service_t_SchedePiatti.delete_piatto_singolo(id=id_piatto_scheda, utenteCancellazione=get_username())
                flash('piatto eliminato con successo!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione del piatto.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori


    else:
        return redirect(url_for('app_cucina.login'))









@app_cucina.route('/ordini/schede_piatti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>', methods=['GET', 'POST'])
@app_cucina.route('/ordini/schede_piatti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>/<int:ordine_id>', methods=['GET', 'POST'])
def ordine_schede_piatti(id, servizio, reparto, scheda, ordine_id=None):
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

        ordine_data = get_data['data']
        year = ordine_data.year
        month = ordine_data.month
        day = ordine_data.day

        id_menu = service_t_Menu.get_by_data(ordine_data, scheda['fkTipoMenu'])
        if 'Error' in id_menu:
            print("Error retrieving menu:", id_menu)
        else:
            menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(id_menu['id'], servizio)
            
            if isinstance(menu_servizio, dict) and 'id' in menu_servizio:
                menu_associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_servizio['id'])
                
                preparazioni_map = {}  # Inizializza la mappa

                for assoc in menu_associazioni:
                    if isinstance(assoc, dict) and 'id' in assoc:
                        assoc_id = assoc['id']
                    else:
                        assoc_id = assoc  # Supponiamo che assoc sia già l'ID
                    
                    fk_associazione_result = service_t_AssociazionePiattiPreparazionie.get_by_id(assoc_id)

                    if isinstance(fk_associazione_result, tuple):
                        fk_associazione = fk_associazione_result[0]
                    else:
                        fk_associazione = fk_associazione_result

                    if fk_associazione and isinstance(fk_associazione, dict) and 'Error' not in fk_associazione:
                        fk_piatto = fk_associazione['fkPiatto']
                        fk_preparazione = fk_associazione.get('fkPreparazione')
                        descrizione_preparazione = preparazioni_map.get(fk_piatto, service_t_preparazioni.get_descrizione_by_id(fk_preparazione))  # Usa la descrizione dalla mappa preparazioni
                        preparazioni_map[fk_piatto] = descrizione_preparazione
                    else:
                        print(f"Errore nella fk_associazione: {fk_associazione}")  # Stampa l'errore per il debug

        form = ordineSchedaForm()
        
        piatti_map = {}
        for piatto in piatti:
            piatto_id = int(piatto['id'])
            piatti_map[piatto_id] = {
                'id': piatto['id'],
                'titolo': preparazioni_map.get(piatto_id, piatto['titolo']),  # Usa la descrizione della preparazione se disponibile
                'codice': piatto['codice'],
                'fkTipoPiatto': piatto['fkTipoPiatto']
            }

        # Recupera i dettagli dell'ordine per il giorno e il reparto specifico
        dettagli_ordine = service_t_OrdiniSchede.get_all_by_day_and_reparto(ordine_data, reparto, servizio, scheda['id'])

        # Lista di tutti gli ID disponibili
        lista_id_disponibili = [ordine['id'] for ordine in dettagli_ordine]

        lista_id_disponibili.insert(0, 0)

        if ordine_id is None or ordine_id == 0:
                # Se non c'è un ordine_id valido o è "new", prepara una scheda vuota
            info_utente = {
                    'nome': '',
                    'cognome': '',
                    'letto': '',
                    'note': ''
                }
            info_piatti = []
            prev_order_id = None
            next_order_id = lista_id_disponibili[1] if len(lista_id_disponibili) > 1 else None


        if len(lista_id_disponibili) > 0:
            if ordine_id is None or ordine_id not in lista_id_disponibili:
                # Se non c'è un ordine_id valido, seleziona il primo ordine come ordine_id predefinito
                ordine_id = lista_id_disponibili[0]

            # Trova l'indice dell'ordine corrente
            current_index = lista_id_disponibili.index(ordine_id)
            prev_order_id = lista_id_disponibili[current_index - 1] if current_index > 0 else None
            next_order_id = lista_id_disponibili[current_index + 1] if current_index < len(lista_id_disponibili) - 1 else None
        
            info_utente = service_t_OrdiniSchede.get_by_id(ordine_id)
             
            info_piatti = service_t_OrdiniPiatti.get_all_by_ordine_scheda(ordine_id)

        
        else:
            prev_order_id, next_order_id = None, None


        if form.validate_on_submit():
            fkOrdine = id
            fkReparto = reparto
            data = get_data['data']
            fkServizio = servizio
            fkScheda = scheda['id']
            letto = form.letto.data

            # Verifica personalizzata
            if service_t_OrdiniSchede.check_letto(fkOrdine, fkReparto, data, fkServizio, fkScheda, letto):
                form.letto.errors.append('Esiste già un record con questi dati. Modifica il record esistente o inserisci nuovi dati.')
                return render_template('ordine_schede_piatti.html',
                                    form=form,
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
                                    servizio=servizio,
                                    prev_order_id=prev_order_id,
                                    next_order_id=next_order_id,
                                    reparto=reparto,
                                    dettagli_ordine=dettagli_ordine,
                                    info_utente=info_utente,
                                    info_piatti=info_piatti,
                                    ordine_id=ordine_id
                                    )

            ordine_id = request.form.get('ordine_id', default=None, type=int)

    # Il resto del codice per la gestione dell'ordine

            if ordine_id and ordine_id != 0:
                service_t_OrdiniPiatti.delete_by_fkOrdine(ordine_id)
                service_t_OrdiniSchede.delete(ordine_id, utenteCancellazione=get_username())

            # Creazione di un nuovo ordine
            new_scheda_ordine = service_t_OrdiniSchede.create(
                fkOrdine=id,
                fkReparto=reparto,
                data=get_data['data'],
                fkServizio=servizio,
                fkScheda=scheda['id'],
                cognome=form.cognome.data,
                nome=form.nome.data,
                letto=form.letto.data,
                utenteInserimento=get_username()
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


        return render_template('ordine_schede_piatti.html',
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
            reparto=reparto,
            dettagli_ordine=dettagli_ordine,
            info_utente=info_utente,
            info_piatti=info_piatti,
            ordine_id=ordine_id
        )
    else:
        return redirect(url_for('app_cucina.login'))




@app_cucina.route('/ordini/print/<int:id>', methods=['GET', 'POST'])
def print_ordini(id):
    if 'authenticated' in session:
        # Recupera tutti gli ordini associati all'ID fornito
        tutti_gli_ordini = service_t_OrdiniSchede.get_all_by_ordine(id)

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
    if 'authenticated' in session:
        # Passo 1: Ottieni i dati dell'ordine
        ordine = service_t_Ordini.get_by_id(id)
        schede = service_t_OrdiniSchede.get_all_by_ordine(id)
        preparazioni = service_t_preparazioni.get_all_preparazioni()
        piatti = service_t_Piatti.get_all()
        reparti = service_t_Reparti.get_all()

        preparazioni_map = {prep['id']: prep['descrizione'] for prep in preparazioni}
        reparti_map = {reparto['id']: reparto['descrizione'] for reparto in reparti}
        piatti_map = {piatto['id']: piatto['titolo'] for piatto in piatti}

        piatti_count = {reparto['id']: {} for reparto in reparti}
        used_preparazioni = set()

        for scheda in schede:
            # Passo 2: Ottieni il giorno e il servizio del menu
            menu_by_scheda = service_t_Schede.get_by_id(scheda['fkScheda'])
            tipo_menu = service_t_Menu.get_by_data(ordine['data'], menu_by_scheda['fkTipoMenu'])
            tipo_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio_per_stampa(tipo_menu['id'], ordine['fkServizio'])

            if tipo_servizio:
                tipo_servizio = tipo_servizio[0]
                piatti_del_menu = service_t_MenuServiziAssociazione.get_info_by_fk_menu_servizio(tipo_servizio['id'])

                associazioni_valide = {item['fkAssociazione'] for item in piatti_del_menu}
                piatti_ordinati = service_t_OrdiniPiatti.get_all_by_ordine_scheda(scheda['id'])

                for piatto_ordinato in piatti_ordinati:
                    fkPiatto = piatto_ordinato['fkPiatto']
                    quantità = piatto_ordinato['quantita']

                    tutte_associazioni = service_t_AssociazionePiattiPreparazionie.get_preparazione_by_piatto(fkPiatto)
                    associazioni_filtrate = [assoc for assoc in tutte_associazioni if assoc['id'] in associazioni_valide]

                    for assoc in associazioni_filtrate:
                        fkPreparazione = assoc['fkPreparazione']
                        preparazione_nome = preparazioni_map.get(fkPreparazione, "Non Disponibile")

                        if preparazione_nome not in piatti_count[scheda['fkReparto']]:
                            piatti_count[scheda['fkReparto']][preparazione_nome] = 0
                        piatti_count[scheda['fkReparto']][preparazione_nome] += quantità
                        used_preparazioni.add(fkPreparazione)

                    if not associazioni_filtrate:
                        piatto_nome = piatti_map.get(fkPiatto, "Non Disponibile")
                        if piatto_nome not in piatti_count[scheda['fkReparto']]:
                            piatti_count[scheda['fkReparto']][piatto_nome] = 0
                        piatti_count[scheda['fkReparto']][piatto_nome] += quantità

        
       # Calcolo dei totali per preparazioni
        preparazioni_totals = {preparazione: 0 for preparazione in set(p for d in piatti_count.values() for p in d.keys())}
        for counts in piatti_count.values():
            for preparazione_nome, count in counts.items():
                if preparazione_nome in preparazioni_totals:
                    preparazioni_totals[preparazione_nome] += count

        # Calcolo del totale aziendale
        totale_azienda = sum(count for counts in piatti_count.values() for count in counts.values())

        print("Piatti Count:", piatti_count)
        print("Preparazioni Totals:", preparazioni_totals)
        print("Totale Azienda:", totale_azienda)

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
        return redirect(url_for('app_cucina.login'))

















    
@app_cucina.route('/ordini', methods=['GET', 'POST'])
def ordini():
    if 'authenticated' in session:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        day = request.args.get('day', datetime.now().day, type=int)
        servizio_corrente = request.args.get('servizio', '1')
        
 
        data = f'{year}-{month}-{day}'

        
        # Ottieni la lista dei reparti dell'utente
        user_reparti_ids = service_t_utenti.get_reparti_list(session['user_id'])
        # Recupera i reparti in base alla lista degli ID
        if user_reparti_ids:
            response = service_t_Reparti.get_by_ids(user_reparti_ids)
            if 'Error' in response:
                return jsonify(response), 400
            reparti = response['results']
        else:
            reparti = service_t_Reparti.get_all()  # Se la lista è vuota, prendi tutti i reparti


        servizio = service_t_Servizi.get_all_servizi()
        schede = service_t_Schede.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_alimentazione = service_t_TipiAlimentazione.get_all()
        ordiniSchede = service_t_OrdiniSchede.get_all_by_day(year, month, day, servizio_corrente)
        schede_attive = service_t_Schede.get_all_attivi_pazienti()

        schede_count, reparti_totals, schede_totals, total_general = service_t_OrdiniSchede.get_ordini_data(
            year, month, day, servizio_corrente, reparti, schede_attive
        )

        ordine_esistente = service_t_Ordini.existing_Ordine(data, servizio_corrente)
        print (ordine_esistente)
        # Se non esiste, crea un nuovo ordine
        if not ordine_esistente:
            service_t_Ordini.create(data, servizio_corrente)
            return redirect(url_for('app_cucina.ordini',servizio_corrente=servizio_corrente, year=year, month=month, day=day))
        

        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}
        tipi_alimentazione_map = {int(tipo_alimentazione['id']): tipo_alimentazione['descrizione'] for tipo_alimentazione in tipi_alimentazione}
        schede_map = {int(scheda['id']): tipi_menu_map[int(scheda['fkTipoMenu'])] for scheda in schede}
        reparti_map = {int(reparto['id']): reparto['descrizione'] for reparto in reparti}

        form = ordineSchedaForm()


        return render_template('ordini.html',
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
    if 'authenticated' in session:
        try:
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


                    # Chiamata al servizio per creare l'utente
                    service_t_utenti.create_utente(
                        username=username,
                        nome=nome,
                        cognome=cognome,
                        fkTipoUtente=fkTipoUtente,
                        fkFunzCustom=fkFunzCustom,
                        reparti=reparti,
                        email=email,
                        password=password
                    )

                    flash('Utente creato con successo!', 'success')
                    return redirect(url_for('app_cucina.creazione_utenti'))

                except Exception as e:
                    print(f'Errore durante la creazione dell\'utente: {str(e)}')  # Stampa per debug
                    flash(f'Errore durante la creazione dell\'utente: {str(e)}', 'error')
            else:
                # Visualizza gli errori di validazione
                error_messages = ', '.join(f"{field}: {', '.join(errors)}" for field, errors in form.errors.items())
                flash(f"Validation errors: {error_messages}", 'error')

            return render_template('creazione_utenti.html',
                                   utenti=utenti,
                                   tipologieUtente=tipologieUtente,
                                   reparti=reparti,
                                   form=form,
                                   tipologieUtente_map=tipologieUtente_map,
                                   reparti_map=reparti_map)
        except Exception as e:
            print(f'Errore generale nella funzione: {str(e)}')  # Stampa per debug
            flash(f'Errore generale: {str(e)}', 'error')
            return redirect(url_for('app_cucina.login'))
    else:
        return redirect(url_for('app_cucina.login'))









@app_cucina.route('/creazione_tipologia_utenti', methods=['GET', 'POST'])
def creazione_tipologia_utenti():
    if 'authenticated' in session:
        tipologieUtente = service_t_tipiUtenti.get_tipiUtenti_all()
        funzionalita_per_tipologia = {}

        for tipo_utente in tipologieUtente:
            funzionalita_utente = service_t_FunzionalitaUtente.get_funz_utenti_by_user_type(tipo_utente['id'])
            funzionalita_per_tipologia[tipo_utente['id']] = funzionalita_utente

        funzionalita = service_t_funzionalita.get_all_menus()
        funzionalita_map = {int(funz['id']): funz['titolo'] for funz in funzionalita}

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
                print(nuovo_tipo_utente_id, funz_id, permesso)
                service_t_FunzionalitaUtente.create(nuovo_tipo_utente_id, funz_id, permesso)

            print('Tipo Utente:', tipo_utente)
            print('Funzionalità Selezionate:', funzionalita_selezionate)
            print('Permessi:', permessi)
            return redirect(url_for('app_cucina.creazione_tipologia_utenti'))

        return render_template('creazione_tipi_utenti.html',
                               tipologieUtente=tipologieUtente,
                               funzionalita_map=funzionalita_map,
                               form=TipoUtenteForm(),
                               funzionalita_per_tipologia=funzionalita_per_tipologia
                               )
    else:
        return redirect(url_for('app_cucina.login'))




@app_cucina.route('/creazione_tipologia_utenti/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def modifica_tipo_utente(id):
    if 'authenticated' in session:
        if request.method == 'GET':
            tipo_utente = service_t_tipiUtenti.get_by_id(id)
            funzionalita_associate = service_t_FunzionalitaUtente.get_funz_utenti_by_user_type(id)
            funzionalita = service_t_funzionalita.get_all_menus()
            funzionalita_map = {int(funz['id']): funz['titolo'] for funz in funzionalita}

            form = TipoUtenteForm(obj=tipo_utente)

            # Stampa il JSON per debug
            print('Tipo Utente:', tipo_utente)
            print('Funzionalità:', funzionalita_map)
            print('Funzionalità Associate:', funzionalita_associate)

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
                    print(id, funz_id, permesso)
                    service_t_FunzionalitaUtente.create(id, funz_id, permesso)

                return jsonify({'message': 'Tipo utente aggiornato con successo!'}), 200

            except Exception as e:
                print(f"Errore durante l'aggiornamento: {e}")
                return jsonify({'Error': 'Errore durante l\'aggiornamento'}), 500




        if request.method == 'DELETE':
            # Gestione della richiesta DELETE, se necessario
            print(f"Request to delete scheda with ID: {id}")  # Aggiungi questo log
            try:
                service_t_FunzionalitaUtente.delete_by_tipo_utente(tipo_utente_id=id)
                service_t_tipiUtenti.delete_tipoUtente(id=id)
                flash('Scheda eliminata con successo!', 'success')
                return '', 204  # Status code 204 No Content per operazioni riuscite senza contenuto da restituire
            except Exception as e:
                print(f"Error deleting scheda: {e}")  # Log per l'errore
                flash('Errore durante l\'eliminazione della scheda.', 'danger')
                return '', 400  # Status code 400 Bad Request per errori

    else:
        return redirect(url_for('app_cucina.login'))







@app_cucina.route('/qualifiche', methods=['GET', 'POST'])
def qualifiche():
    if 'authenticated' in session:

 


        return render_template('qualifiche.html',
                              
                               )
    else:
        return redirect(url_for('app_cucina.login'))

















@app_cucina.route('/do_logout', methods=['POST'])
def do_logout():
    form = LogoutFormNoCSRF()
    if form.validate_on_submit():
        service_t_utenti.do_logout_nuovo(session['user_id'])
        session.clear()
        return jsonify({'message': 'Successfully logged out.'}), 200
    return jsonify({'error': 'Invalid request.'}), 400



# Register the blueprint
app.register_blueprint(app_cucina, url_prefix='/app_cucina')

if __name__ == '__main__':
    app.run(debug=True)


