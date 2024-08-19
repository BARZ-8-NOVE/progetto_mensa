

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
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import TFunzionalitaUtenteService
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseDB.config import DATABASE_URI, SECRET_KEY
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseForm.form import AlimentiForm, PreparazioniForm, AlimentoForm, PiattiForm, MenuForm, LoginFormNoCSRF, LogoutFormNoCSRF, schedaForm, ordineSchedaForm
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

service_t_SchedePiatti = Service_t_SchedePiatti()
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

            # Restituisce i dettagli della preparazione e gli ingredienti
            return jsonify({
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
            })

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

@app_cucina.route('/ordini_schede_piatti/<int:id>/<int:servizio>/<int:reparto>/<int:scheda>', methods=['GET', 'POST'])
def ordine_schede_piatti(id, servizio, reparto, scheda):
    if 'authenticated' in session:
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(scheda, servizio)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(scheda, servizio)
        get_data = service_t_Ordini.get_by_id(id)
        scheda = service_t_Schede.get_by_id(scheda)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        info_servizio = service_t_Servizi.get_servizio_by_id(servizio)
        info_reparto = service_t_Reparti.get_by_id(reparto)
        tipi_piatti = service_t_TipiPiatti.get_all()
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}

        form = ordineSchedaForm()

        piatti_map = {int(piatto['id']): {'id': piatto['id'], 'titolo': piatto['titolo'], 'codice': piatto['codice'], 'fkTipoPiatto': piatto['fkTipoPiatto']} for piatto in piatti}

        if form.validate_on_submit():
            # Inserimento dei dati nel database
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
            print (piatti_list)
            for piatto in piatti_list:
                try:
                    # Save ingredient
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
            return redirect(url_for('app_cucina.ordini'))  # Redirect to the list of preparations

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
                               form=form)
    else:
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/schede_piatti/<int:id>', methods=['GET', 'POST'])
def schede_piatti(id):
    if 'authenticated' in session:
        servizio_corrente = request.args.get('servizio', '1')
        scheda = service_t_Schede.get_by_id(id)
        piatti = service_t_Piatti.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        schedePiatti = service_t_SchedePiatti.get_piatti_non_dolci_by_scheda(id,servizio_corrente)
        schedeDolci = service_t_SchedePiatti.get_dolci_pane_by_scheda(id,servizio_corrente)
        servizi = service_t_Servizi.get_all_servizi()
        tipi_piatti = service_t_TipiPiatti.get_all()
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}

        piatti_map = {int(piatto['id']): {'titolo': piatto['titolo'], 'codice': piatto['codice'], 'fkTipoPiatto': piatto['fkTipoPiatto']} for piatto in piatti}

        return render_template('schede_piatti.html',
                               scheda=scheda,
                               piatti=piatti,
                               servizi=servizi,
                               schedePiatti=schedePiatti,
                               tipi_piatti=tipi_piatti,
                               piatti_map=piatti_map,
                               tipi_menu_map=tipi_menu_map,
                               schedeDolci=schedeDolci)
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


        servizio = service_t_Servizi.get_all_servizi()
        schede = service_t_Schede.get_all()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_alimentazione = service_t_TipiAlimentazione.get_all()
        reparti = service_t_Reparti.get_all()
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


# @app_cucina.route('/ordini/<int:id_ordine>, <int:id_reparto>, <int:id_scheda>', methods=['GET', 'POST', 'DELETE'])
# def ordini_schede(id_ordine,id_servizio, id_reparto,id_scheda ):

#     if 'authenticated' in session:

#         form = ordineSchedaForm()

#         if request.method == 'GET':


#             ordineScheda = service_t_OrdiniSchede.get_by_ordine_reparto_scheda(id_ordine,id_reparto,id_scheda)
#             if not ordineScheda:
#                 flash('Scheda non trovata!', 'danger')
#                 return redirect(url_for('app_cucina.schede'))

#             return jsonify({
#                 'fkOrdine': ordineScheda.get('fkOrdine'),
#                 'fkReparto': ordineScheda.get('fkReparto'),
#                 'data': ordineScheda.get('data').strftime('%Y-%m-%d'),
#                 'fkServizio': ordineScheda.get('fkServizio'),
#                 'fkScheda': ordineScheda.get('fkScheda'),
#                 'cognome': ordineScheda.get('cognome'),
#                 'nome': ordineScheda.get('nome'),
#                 'letto': ordineScheda.get('letto'),
#                 'dataInserimento': ordineScheda.get('dataInserimento'),
#                 'utenteInserimento': ordineScheda.get('utenteInserimento')


#             })
        


#     else:
#         return redirect(url_for('app_cucina.login'))


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


