

#from Classi.initialize_db.initialize_db import initialize_database
# Inizializzare il database
#initialize_database()

# Importare i controller
# from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
# from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
# from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import TFunzionalitaUtenteService
# from Classi.ClasseUtenti.Classe_t_autorizzazioni.Service_t_autorizzazioni import Service_t_autorizzazioni
# from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti


from Classi.ClasseAlimenti.Classe_t_alimenti.Service_t_alimenti import ServiceAlimenti
from Classi.ClasseAlimenti.Classe_t_allergeni.Service_t_allergeni import ServiceAllergeni
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Service_t_tipologiaalimenti import Service_t_tipologiaalimenti
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Service_t_tipologiaconservazione import ServiceTipologiaConservazioni

from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Service_t_tipoPreparazioni import Service_t_tipipreparazioni
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Service_t_Preparazioni import Service_t_preparazioni
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Service_t_tipiquantita import Service_t_tipoquantita
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Service_t_preparazioniContenuti import Service_t_preparazionicontenuti


# from Classi.ClasseReparti.Service_t_reparti import ServiceReparti

# from Classi.ClasseOrdini.Classe_t_ordini.Service_t_ordini import ServiceOrdini
# from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Service_t_ordiniPiatti import ServiceOrdiniPiatti
# from Classi.ClasseUtility import *

# from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
# from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, Blueprint, request, session, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies
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
from Classi.ClasseForm.form_alimenti import AlimentiForm, PreparazioniForm, AlimentoForm
# Initialize the app and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)

# Initialize JWT and CORS
jwt = JWTManager(app)
CORS(app)

# Initialize services
service_t_utenti = Service_t_utenti()

serviceAlimenti = ServiceAlimenti()
service_t_tipologiaalimenti = Service_t_tipologiaalimenti()
serviceAllergeni = ServiceAllergeni()

service_t_preparazioni = Service_t_preparazioni()
service_t_preparazionicontenuti = Service_t_preparazionicontenuti()
service_t_tipipreparazioni = Service_t_tipipreparazioni()
service_t_tipoquantita = Service_t_tipoquantita()

# Define the blueprint
app_cucina = Blueprint('app_cucina', __name__, template_folder='template')

# Background job for removing expired tokens
def remove_expired_tokens():
    service_t_utenti.expiredTokens()

scheduler = BackgroundScheduler()
scheduler.add_job(func=remove_expired_tokens, trigger="interval", seconds=60)
scheduler.start()

# Handle expired JWT tokens
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    current_utente_public_id = jwt_payload['sub']
    service_t_utenti.do_logout(current_utente_public_id)  # Deactivate user
    response = jsonify({"message": "Logged out because the token has expired."})
    unset_jwt_cookies(response)
    return response



@app_cucina.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            dati = request.form
            required_fields = ['username', 'password']
            UtilityGeneral.check_fields(dati, required_fields)
            
            username = dati['username']
            password = dati['password']

            user = service_t_utenti.do_login(username, password)
            if user:
                session['authenticated'] = True
                session['user_id'] = user['id']
                session['token'] = user['token']
                
                funzionalita_service = TFunzionalitaUtenteService()
                menu_structure = funzionalita_service.build_menu_structure(user['id'])
                session['menu_structure'] = menu_structure
                
                # Redirect to index with token in session
                return redirect(url_for('app_cucina.index'))

            else:
                flash('Invalid username or password', 'error')
                return render_template('loginx.html')
        
        except Exception as e:
            print(f"Error during login: {e}")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('loginx.html')
    
    return render_template('loginx.html')  # GET request

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

    return dict(
        menu_structure=menu_structure,
        username=username,
        token=token
    )


@app_cucina.route('/index')
def index():
    if 'authenticated' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('app_cucina.login'))


@app_cucina.route('/alimenti', methods=['GET', 'POST'])
def alimenti():
    # Retrieve the list of alimenti, tipologie, and allergeni from your database
    alimenti_list = serviceAlimenti.get_all()
    tipologie = service_t_tipologiaalimenti.get_all_tipologiaalimenti()
    allergeni = serviceAllergeni.get_all()
    
    # Create maps for tipologie and allergeni
    tipologie_map = {int(tipologia['id']): tipologia['nome'] for tipologia in tipologie}
    allergeni_map = {str(allergene['id']): allergene['nome'] for allergene in allergeni}

    form = AlimentiForm()
    form.fkAllergene.choices = [(allergene['id'], allergene['nome']) for allergene in allergeni]
    form.fkTipologiaAlimento.choices = [(tipologia['id'], tipologia['nome']) for tipologia in tipologie]

    if 'authenticated' in session:
        if form.validate_on_submit():
            fkAllergene = ",".join(str(allergene_id) for allergene_id in form.fkAllergene.data)

            serviceAlimenti.create(
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

@app_cucina.route('/preparazioni', methods=['GET', 'POST'])
def preparazioni():
    preparazioni = service_t_preparazioni.get_all_preparazioni()
    tipiPreparazioni = service_t_tipipreparazioni.get_all_tipipreparazioni()
    preparazioniContenuti = service_t_preparazionicontenuti.get_all_preparazioni_contenuti()

    # Get alimenti and tipi_quantita using the appropriate methods
    alimenti = serviceAlimenti.get_all()  # Assuming this method returns a list of alimenti
    tipi_quantita = service_t_tipoquantita.get_all_tipoquantita()  # Assuming this returns a list

    form = PreparazioniForm()
    alimform = AlimentoForm()
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

            ingredient_list = request.form.getlist('ingredientList')
            for ingredient in ingredient_list:
                ingredient_data = json.loads(ingredient)
                service_t_preparazionicontenuti.create_preparazioni_contenuti(
                    fkPreparazione=new_preparazione_id, 
                    fkAlimento=ingredient_data['fkAlimento'], 
                    quantita=ingredient_data['quantita'], 
                    fkTipoQuantita=ingredient_data['fkTipoQuantita'], 
                    note=ingredient_data['note'],   
                    utenteInserimento=utente_inserimento
                )

            flash('Preparazione aggiunta con successo!', 'success')
            return redirect(url_for('app_cucina.preparazione_dettagli', id_preparazione=new_preparazione_id))

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
            tipo_map=tipo_map

        )
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('app_cucina.login'))



@app_cucina.route('/preparazione_dettagli/<int:id_preparazione>', methods=['GET'])
def preparazione_dettagli(id_preparazione):
    preparazione = service_t_preparazioni.get_preparazione_by_id(id_preparazione)
    preparazione_contenuti = service_t_preparazionicontenuti.get_preparazioni_contenuti_by_id_preparazione(id_preparazione)

    if preparazione:
        return render_template('preparazione_dettagli.html', preparazione=preparazione, preparazione_contenuti=preparazione_contenuti)
    else:
        return redirect(url_for('app_cucina.preparazioni'))





@app_cucina.route('/do_logout', methods=['POST'])
@jwt_required()
def do_logout():
    try:
        current_utente_public_id = get_jwt_identity()
        service_t_utenti.do_logout(current_utente_public_id)
        session.clear()
        return jsonify({'message': 'Successfully logged out.'}), 200 
    except NotFound as e:
        return jsonify({'Error': str(e)}), 404
    except KeyError as e:
        return jsonify({'Error': str(e)}), 400
    except Forbidden as e:
        return jsonify({
            'Error': str(e),
            'redirect': url_for('app_cucina.login')  # Redirect URL
        }), 403
    except Exception as e:
        # Handle token expiration separately
        if isinstance(e, jwt.ExpiredSignatureError):
            return jsonify({
                'Error': 'Token has expired. You will be redirected to the login page.',
                'redirect': url_for('app_cucina.login')
            }), 403
        return jsonify({'Error': str(e)}), 500





# Register the blueprint
app.register_blueprint(app_cucina, url_prefix='/app_cucina')

if __name__ == '__main__':
    app.run(debug=True)
