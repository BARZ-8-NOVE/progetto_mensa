

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

from Classi.ClasseServizi.Service_t_servizi import Service_t_Servizi
from Classi.ClasseReparti.Service_t_reparti import Service_t_Reparti

from Classi.ClasseOrdini.Classe_t_ordini.Service_t_ordini import ServiceOrdini
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Service_t_ordiniPiatti import ServiceOrdiniPiatti
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
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import TFunzionalitaUtenteService
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseDB.config import DATABASE_URI, SECRET_KEY
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseForm.form import AlimentiForm, PreparazioniForm, AlimentoForm, PiattiForm, MenuForm, LoginFormNoCSRF, LogoutFormNoCSRF
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


@app_cucina.before_request
def check_token():
    # Elenco delle rotte esenti dal controllo del token
    exempt_routes = ['app_cucina.login', 'app_cucina.index']

    # Se la rotta corrente è esente, salta il controllo del token
    if request.endpoint in exempt_routes:
        return

    # Verifica se l'utente è autenticato
    if 'authenticated' not in session or session.get('authenticated') is False:
        return redirect(url_for('app_cucina.login'))

    # Verifica la validità del token JWT
    try:
        user_id = session.get('user_id')
        # Controlla nel database se il token è ancora valido
        if not service_t_utenti.is_token_valid(user_id, session.get('token')):
            session['authenticated'] = False
            return redirect(url_for('app_cucina.login'))
    except Exception as e:
        session['authenticated'] = False
        return redirect(url_for('app_cucina.login'))

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
                
                funzionalita_service = TFunzionalitaUtenteService()
                menu_structure = funzionalita_service.build_menu_structure(user['id'])
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




        

# @app_cucina.route('/login', methods=['GET', 'POST'])

# def login():
#     if request.method == 'POST':
#         try:
#             dati = request.form
#             required_fields = ['username', 'password']
#             UtilityGeneral.check_fields(dati, required_fields)
            
#             username = dati['username']
#             password = dati['password']

#             user = service_t_utenti.do_login(username, password)
#             if user:
#                 session['authenticated'] = True
#                 session['user_id'] = user['id']
#                 session['token'] = user['token']
                
#                 funzionalita_service = TFunzionalitaUtenteService()
#                 menu_structure = funzionalita_service.build_menu_structure(user['id'])
#                 session['menu_structure'] = menu_structure
                
#                 # Redirect to index with token in session
#                 return redirect(url_for('app_cucina.index'))

#             else:
#                 flash('Invalid username or password', 'error')
#                 return render_template('loginx.html')
        
#         except Exception as e:
#             print(f"Error during login: {e}")
#             flash('An error occurred during login. Please try again.', 'error')
#             return render_template('loginx.html')
    
#     return render_template('loginx.html')  # GET request

def get_username():
    user_id = session.get('user_id')
    user = service_t_utenti.get_utente_by_id(user_id)
    
    return user['username']

@app.context_processor
def inject_user_data():

    menu_structure = session.get('menu_structure', [])
    user_id = session.get('user_id')
    user = service_t_utenti.get_utente_by_id(user_id) if user_id else None
    
    username = user['username'] if user else "Utente"
    token = session.get('token')

    form = LogoutFormNoCSRF()

    return dict(
        menu_structure=menu_structure,
        username=username,
        token=token,
        form=form
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

    if 'authenticated' in session:
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

@app_cucina.route('/get_tipi_piatti/<int:fkTipoPreparazione>', methods=['GET'])
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



@app_cucina.route('/preparazioni/<int:id_preparazione>', methods=['GET'])
def preparazione_dettagli(id_preparazione):
    # Recupera la preparazione basata sull'ID fornito
    preparazione = service_t_preparazioni.get_preparazione_by_id(id_preparazione)
    
    if not preparazione:
        flash('Preparazione non trovata.', 'danger')
        return redirect(url_for('app_cucina.preparazioni'))


    # Recupera tutti i tipi di preparazione disponibili
    tipiPreparazioni = service_t_tipipreparazioni.get_all_tipipreparazioni()
    
    # Recupera tutti gli alimenti disponibili
    alimenti = service_t_Alimenti.get_all()
    
    # Recupera tutti i contenuti di preparazione per l'ID preparazione specificato
    alimentiPerPrep = service_t_preparazionicontenuti.get_preparazioni_contenuti_by_id_preparazione(id_preparazione)
    
    # Recupera tutti i tipi di quantità disponibili
    tipi_quantita = service_t_tipoquantita.get_all_tipoquantita()

    # Costruisci il mapping degli alimenti per ID
    alimento_map = {int(alimento['id']): alimento['alimento'] for alimento in alimenti}
    
    # Costruisci il mapping dei tipi di preparazione per ID
    TipoPreparazione_map = {int(tipoPreparazione['id']): tipoPreparazione['descrizione'] for tipoPreparazione in tipiPreparazioni}
    
    # Costruisci il mapping dei tipi di quantità per ID
    tipo_map = {int(tipo_quantita['id']): tipo_quantita['tipo'] for tipo_quantita in tipi_quantita}
    
    # Costruisci il mapping dei contenuti di preparazione per ID di alimento
    prep_map = {int(contenuto['fkAlimento']): alimento_map[int(contenuto['fkAlimento'])] for contenuto in alimentiPerPrep}

    # Passa i dati al template
    return render_template('dettaglio_preparazione.html', 
                           alimentiPerPrep=alimentiPerPrep,
                           preparazione=preparazione,
                           TipoPreparazione_map=TipoPreparazione_map,
                           alimento_map=alimento_map,
                           prep_map=prep_map,
                           tipo_map=tipo_map)







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

            # Mostra il template con i dati aggiornati
            return render_template('piatti.html',
                                   piatti=piatti,
                                   tipologia_piatti=tipologia_piatti,
                                   TipoPiatto_map=TipoPiatto_map,
                                   form=form)
    
    # Se il form non è stato inviato o non è valido, mostra il template con il form vuoto o con errori
        return render_template('piatti.html',
                           piatti=piatti,
                           tipologia_piatti=tipologia_piatti,
                           TipoPiatto_map=TipoPiatto_map,
                           form=form)
    
    # Se l'utente non è autenticato, reindirizzalo alla pagina di login
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
    # Ottieni i parametri dai query string
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    tipo_menu = request.args.get('tipo_menu', '1')

    cal = calendar.Calendar(firstweekday=0)  # 0 per lunedì, 6 per domenica
    month_days = cal.monthdayscalendar(year, month)
    month_name = calendar.month_name[month]

    # Mappa per i giorni della settimana
    weekdays = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

    utente_inserimento = get_username()
    # Recupera i dati dal servizio
    tipologie_menu = service_t_TipiMenu.get_all()
    menu = service_t_Menu.get_by_month(year, month, tipo_menu)
    associazione = service_t_AssociazionePiattiPreparazionie.get_all()
    piatti = service_t_Piatti.get_all()
    preparazioni = service_t_preparazioni.get_all_preparazioni()
    servizi = service_t_Servizi.get_all_servizi()
    
    # Recupera gli ID dei menu filtrati per il mese corrente
    menu_ids = [m.get('id') for m in menu if m.get('id') is not None]

    # Crea menu e servizi se non ci sono abbastanza menu per tutti i giorni del mese
    if len(menu_ids) < len(month_days):
        for week in month_days:
            for day in week:
                if day != 0:  # Salta i giorni che sono parte del mese precedente o successivo
                    # Controlla se esiste già un menu per il giorno corrente
                    existing_menu = service_t_Menu.get_by_date_and_type(year, month, day, tipo_menu)
                    if not existing_menu:
                        # Crea un nuovo menu
                        new_menu_id = service_t_Menu.create(date(year, month, day), tipo_menu, utente_inserimento)
                        if new_menu_id:
                            # Popola il nuovo menu con i servizi
                            for servizio in servizi:
                                new_servizio_id = service_t_MenuServizi.create(new_menu_id, servizio['id'], utente_inserimento)
                                
                                old_menu = service_t_Menu.get_by_date_and_type_previous_year(year, month, day, tipo_menu)
                                if old_menu:
                                    old_menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(old_menu.id)
                                    for old_servizio in old_menu_servizi:
                                        if old_servizio['fkServizio'] == servizio['id']:
                                            old_menu_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(old_servizio ['id'])
                                            for old_piatto in old_menu_piatti:
                                                service_t_MenuServiziAssociazione.create(new_servizio_id, old_piatto['id'], utente_inserimento)
        
        # Dopo aver creato i menu, servizi e piatti, fai un redirect alla stessa pagina
        return redirect(url_for('app_cucina.menu', year=year, month=month, tipo_menu=tipo_menu))
                                        

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
        for servizio in servizi:  # Iterate over each service
            servizio_id = menu_servizi_map.get(menu_item['id'], {}).get(servizio['id'])
            menu_per_giorno[date_key][servizio['descrizione']] = servizio_id

    # Recupera i piatti per ogni servizio dinamicamente
    piattimenu = {}
    for servizio_id in set(id for ids in menu_servizi_map.values() for id in ids.values()):
        piattimenu[servizio_id] = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(servizio_id)

    # Crea una mappa dei piatti e delle preparazioni
    piatti_map = {int(piatto['id']): piatto['fkTipoPiatto'] for piatto in piatti}
    preparazioni_map = {int(preparazione['id']): preparazione['descrizione'] for preparazione in preparazioni}
    # piatti_form = {int(piatto['id']): piatto['titolo'] for piatto in piatti}
    # Mappa per associare i piatti e le preparazioni
    associazione_map = {}
    for tipo_associa in associazione:
        piatto_nome = piatti_map.get(tipo_associa['fkPiatto'], 'Sconosciuto')
        preparazione_descrizione = preparazioni_map.get(tipo_associa['fkPreparazione'], 'Sconosciuto')
        associazione_map[tipo_associa['id']] = {
            'piatto': piatto_nome,
            'preparazione': preparazione_descrizione
        }



        

    if 'authenticated' in session:
        return render_template(
            'menu.html',
            year=year,
            month=month,
            month_name=month_name,
            month_days=month_days,
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
            calendar=calendar
        )
    else:
        return redirect(url_for('app_cucina.login'))

@app_cucina.route('/set_menu_id/<int:menuServizio_id>')
def set_menu_id(menuServizio_id):
    session['menu_id'] = menuServizio_id

    associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menuServizio_id)

    # Crea una lista per accumulare gli oggetti prep
    preps = []

    for associazione in associazioni:
        piatto_id = associazione['id']
        prep = service_t_AssociazionePiattiPreparazionie.get_by_id(piatto_id)
        preps.append(prep)  # Aggiungi l'oggetto prep alla lista

    # Restituisci la risposta JSON con la lista di oggetti prep
    return jsonify({
        'menu_id': menuServizio_id,
        'associazion': preps  # Invia l'array di oggetti
    })


@app_cucina.route('/menu/dettagli/<int:id_menu>', methods=['GET', 'POST'])
def menu_dettagli(id_menu):
    if 'authenticated' in session:
        # Recupera le associazioni esistenti
        associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(id_menu)
        
        piatti_e_prep = []
        for associazione in associazioni:
            piatti_e_prep.extend(service_t_AssociazionePiattiPreparazionie.get_by_id_ritorno_diz(associazione['id']))

        tipologia_piatti = service_t_TipiPiatti.get_all()
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
                return redirect(url_for('app_cucina.menu'))
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
                                prep_per_piatto=prep_per_piatto
                                )
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/get_menu_details', methods=['GET'])
def get_menu_details():
    menu_servizio = session.get('menu_id')

    if menu_servizio is None:
        return jsonify({'error': 'ID del menu servizio non trovato nella sessione'}), 400

    associazioni = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_servizio)
    preparazioni = service_t_preparazioni.get_all_preparazioni() 
    piatti = service_t_Piatti.get_all()

    piatti_map = {int(piatto['id']): piatto['fkTipoPiatto'] for piatto in piatti}
    preparazioni_map = {int(preparazione['id']): preparazione['descrizione'] for preparazione in preparazioni}
    dettagli_menu = []
    for associazione in associazioni:
        piatto_id = associazione['id']
        preparazioni = service_t_AssociazionePiattiPreparazionie.get_by_id_ritorno_diz(piatto_id)
        dettagli_menu.append({
            'piatto': piatti_map.get(piatto_id, 'Sconosciuto'),
            'preparazione': preparazioni_map.get(preparazioni['fkPreparazione'], 'Sconosciuto')
        })

    return jsonify(dettagli_menu)



@app_cucina.route('/do_logout', methods=['POST'])
def do_logout():
    form = LogoutFormNoCSRF()
    if form.validate_on_submit():
        service_t_utenti.do_logout_nuovo(session['user_id'])
        session.clear()
        return jsonify({'message': 'Successfully logged out.'}), 200
    return jsonify({'error': 'Invalid request.'}), 400

# @app_cucina.route('/do_logout_vecchio', methods=['POST'])
# @jwt_required()
# def do_logout_veccio():
#     try:
#         current_utente_public_id = get_jwt_identity()
#         service_t_utenti.do_logout(current_utente_public_id)
#         session.clear()
#         return jsonify({'message': 'Successfully logged out.'}), 200 
#     except NotFound as e:
#         return jsonify({'Error': str(e)}), 404
#     except KeyError as e:
#         return jsonify({'Error': str(e)}), 400   
#     except Forbidden as e:
#         return jsonify({
#             'Error': str(e),
#             'redirect': url_for('app_cucina.login')
#         }), 403
#     except jwt.ExpiredSignatureError:
#         return jsonify({
#             'Error': 'Token has expired. You will be redirected to the login page.',
#             'redirect': url_for('app_cucina.login')
#         }), 403
#     except Exception as e:
#         return jsonify({'Error': str(e)}), 500



# Register the blueprint
app.register_blueprint(app_cucina, url_prefix='/app_cucina')

if __name__ == '__main__':
    app.run(debug=True)


