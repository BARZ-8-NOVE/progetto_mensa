from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.config import DATABASE_URI
from Classi.ClasseDB.db_connection import get_db, Base, engine
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Controller_t_Preparazioni import t_preparazioni_controller
from Classi.ClasseAlimenti.Classe_t_alimenti.Controller_t_alimenti import t_alimenti_controller
from Classi.ClasseUtenti.Classe_t_funzionalita.Controller_t_funzionalita import t_funzionalita_controller
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Controller_t_autorizzazioni import t_autorizzazioni_controller
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Controller_t_tipiUtenti import t_tipiUtenti_controller
from Classi.ClasseAlimenti.Classe_t_allergeni.Controller_t_allergeni import t_allergeni_controller
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Controller_t_tipologiaalimenti import t_tipologiaalimenti_controller
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Controller_t_tipologiaconservazione import t_tipologiaconservazioni_controller
from Classi.ClasseUtenti.Classe_t_utenti.Controller_t_utenti import t_utenti_controller
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = engine
app.register_blueprint(t_tipologiaconservazioni_controller, url_prefix='/tipologiaconservazioni')
app.register_blueprint(t_allergeni_controller, url_prefix='/allergeni')
app.register_blueprint(t_tipologiaalimenti_controller, url_prefix='/tipologiaalimenti')
app.register_blueprint(t_alimenti_controller, url_prefix='/alimenti')



app.register_blueprint(t_preparazioni_controller, url_prefix='/preparazioni')

app.register_blueprint(t_funzionalita_controller, url_prefix='/funzionalita')
app.register_blueprint(t_autorizzazioni_controller, url_prefix='/autorizzazioni')
app.register_blueprint(t_tipiUtenti_controller, url_prefix='/tipiUtenti')
app.register_blueprint(t_utenti_controller, url_prefix='/utenti')

if __name__ == '__main__':
    app.run(debug=True)