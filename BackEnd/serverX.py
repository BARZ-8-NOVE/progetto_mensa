

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

# from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Service_t_tipoPreparazioni import Service_t_tipipreparazioni
# from Classi.ClassePreparazioni.Classe_t_Preparazioni.Service_t_Preparazioni import Service_t_preparazioni
# from Classi.ClassePreparazioni.Classe_t_tipiquantita.Service_t_tipiquantita import Service_t_tipoquantita
# from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Service_t_preparazioniContenuti import Service_t_preparazionicontenuti


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

# Import your service modules here
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import TFunzionalitaUtenteService
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseDB.config import DATABASE_URI, SECRET_KEY
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes

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


@app.context_processor
def inject_user_data():
    menu_structure = session.get('menu_structure', [])
    user_id = session.get('user_id')
    user = service_t_utenti.get_utente_by_id(user_id) if user_id else None
    
    username = user['username'] if user else "Utente"
    token = session.get('token', '')
    
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

@app_cucina.route('/alimenti')
def alimenti():
    # Retrieve the list of alimenti, tipologie, and allergeni from your database
    alimenti = serviceAlimenti.get_all()
    tipologie = service_t_tipologiaalimenti.get_all_tipologiaalimenti()
    allergeni = serviceAllergeni.get_all()
    
    
    # Create maps for tipologie and allergeni
    tipologie_map = {int(tipologia['id']): tipologia['nome'] for tipologia in tipologie}
    allergeni_map = {str(allergene['id']): allergene['nome'] for allergene in allergeni}
    
    return render_template(
        'alimenti.html',
        alimenti=alimenti,
        tipologie=tipologie,
        allergeni=allergeni,
        tipologie_map=tipologie_map,
        allergeni_map=allergeni_map,

    )


@app_cucina.route('alimenti/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['alimento', 'energia_Kcal', 'energia_KJ', 'prot_tot_gr', 'glucidi_tot', 'lipidi_tot', 'saturi_tot', 'fkAllergene', 'fkTipologiaAlimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        alimento = dati['alimento'].strip()
        energia_Kcal = float(dati['energia_Kcal'])
        energia_KJ = float(dati['energia_KJ'])
        prot_tot_gr = float(dati['prot_tot_gr'])
        glucidi_tot = float(dati['glucidi_tot'])
        lipidi_tot = float(dati['lipidi_tot'])
        saturi_tot = float(dati['saturi_tot'])
        fkAllergene = dati['fkAllergene'].strip()
        fkTipologiaAlimento = int(dati['fkTipologiaAlimento'])

        return jsonify(serviceAlimenti.create(alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


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
