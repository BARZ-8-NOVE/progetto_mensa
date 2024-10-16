from flask import Flask, jsonify
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.config import DATABASE_URI, SECRET_KEY
from Classi.ClasseDB.db_connection import get_db, Base, engine
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
jwt = JWTManager(app)

#from Classi.initialize_db.initialize_db import initialize_database
# Inizializzare il database
#initialize_database()

# Importare i controller
from Classi.ClasseUtenti.Classe_t_funzionalita.Controller_t_funzionalita import t_funzionalita_controller
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Controller_t_funzionalitaUtente import t_funzionalitaUtenti_controller
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Controller_t_autorizzazioni import t_autorizzazioni_controller
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Controller_t_tipiUtenti import t_tipiUtenti_controller
from Classi.ClasseUtenti.Classe_t_utenti.Controller_t_utenti import t_utenti_controller

from Classi.ClasseAlimenti.Classe_t_alimenti.Controller_t_alimenti import t_alimenti_controller
from Classi.ClasseAlimenti.Classe_t_allergeni.Controller_t_allergeni import t_allergeni_controller
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Controller_t_tipologiaalimenti import t_tipologiaalimenti_controller
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Controller_t_tipologiaconservazione import t_tipologiaconservazioni_controller

from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Controller_t_tipoPreparazioni import t_tipipreparazioni_controller
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Controller_t_Preparazioni import t_preparazioni_controller
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Controller_t_tipiquantita import t_tipoquantita_controller
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Controller_t_preparazioniContenuti import t_preparazionicontenuti_controller

from Classi.ClasseServizi.Controller_t_servizi import t_servizi_controller

from Classi.ClassePiatti.Classe_t_piatti.Controller_t_piatti import t_piatti_controller
from Classi.ClassePiatti.Classe_t_tipiPiatti.Controller_t_tipiPiatti import t_tipi_piatti_controller
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Controller_t_associazionePiattiPreparazioni import t_associazione_controller

from Classi.ClasseMenu.Classe_t_tipiMenu.Controller_t_tipiMenu import t_tipimenu_controller
from Classi.ClasseMenu.Classe_t_menuServizi.Controller_t_menuServizi import t_menu_servizi_controller
from Classi.ClasseMenu.Classe_t_menu.Controller_t_menu import t_menu_controller

from Classi.ClasseReparti.Controller_t_reparti import t_reparti_controller

from Classi.ClasseOrdini.Classe_t_ordiniSchede.Controller_t_ordiniSchede import t_ordiniSchede_controller
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Controller_t_ordiniPiatti import t_ordini_piatti_controller



# Add the parent directory of the current script to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import the FrontEnd module using the full package path
# from progetto_mensa.FrontEnd.Front_end import app_cucina


db = engine
app.register_blueprint(t_tipologiaconservazioni_controller, url_prefix='/tipologiaconservazioni')
app.register_blueprint(t_allergeni_controller, url_prefix='/allergeni')
app.register_blueprint(t_tipologiaalimenti_controller, url_prefix='/tipologiaalimenti')
app.register_blueprint(t_alimenti_controller, url_prefix='/alimenti')

app.register_blueprint(t_servizi_controller, url_prefix='/servizi')

app.register_blueprint(t_preparazioni_controller, url_prefix='/preparazioni')
app.register_blueprint(t_tipoquantita_controller, url_prefix='/tipoquantita')
app.register_blueprint(t_preparazionicontenuti_controller, url_prefix='/preparazionicontenuti')
app.register_blueprint(t_tipipreparazioni_controller, url_prefix='/tipipreparazioni')

app.register_blueprint(t_funzionalita_controller, url_prefix='/funzionalita')
app.register_blueprint(t_funzionalitaUtenti_controller, url_prefix='/funzionalita_utenti')
app.register_blueprint(t_tipiUtenti_controller, url_prefix='/tipiUtenti')
app.register_blueprint(t_utenti_controller, url_prefix='/utenti')
app.register_blueprint(t_autorizzazioni_controller, url_prefix='/autorizzazioni')

app.register_blueprint(t_piatti_controller, url_prefix='/piatti')
app.register_blueprint(t_tipi_piatti_controller, url_prefix='/tipipiatti')
app.register_blueprint(t_associazione_controller, url_prefix='/associazione')

app.register_blueprint(t_tipimenu_controller, url_prefix='/tipimenu')
app.register_blueprint(t_menu_servizi_controller, url_prefix='/menuservizi')
app.register_blueprint(t_menu_controller, url_prefix='/menu')

app.register_blueprint(t_reparti_controller, url_prefix='/reparti')

app.register_blueprint(t_ordiniSchede_controller, url_prefix='/ordiniSchede')
app.register_blueprint(t_ordini_piatti_controller, url_prefix='/ordinipiatti')

# app.register_blueprint(app_cucina, url_prefix='/app_cucina')

#if __name__ == '__main__':
#    app.run(debug=True)