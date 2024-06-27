from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.config import DATABASE_URI
from Classi.ClasseDB.db_connection import get_db, Base, engine
from Classi.ClasseAlimenti.Classe_t_alimenti.Controller_t_alimenti import t_alimenti_controller
from Classi.Classe_t_funzionalita.Controller_t_funzionalita import t_funzionalita_controller
from Classi.Classe_t_autorizzazioni.Controller_t_autorizzazioni import t_autorizzazioni_controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = engine


app.register_blueprint(t_alimenti_controller, url_prefix='/alimenti')
app.register_blueprint(t_funzionalita_controller, url_prefix='/funzionalita')
app.register_blueprint(t_autorizzazioni_controller, url_prefix='/autorizzazioni')

if __name__ == '__main__':
    app.run(debug=True)