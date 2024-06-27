from flask import Flask
from Classi.ClasseDB.config import DATABASE_URI
from Classi.ClasseAlimenti.Classe_t_alimenti.Controller_t_alimenti import t_alimenti_controller
from Classi.Classe_t_funzionalita.Controller_t_funzionalita import t_funzionalita_controller
from Classi.Classe_t_autorizzazioni.Controller_t_autorizzazioni import t_autorizzazioni_controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(t_alimenti_controller, url_prefix='/alimenti')
app.register_blueprint(t_funzionalita_controller, url_prefix='/funzionalita')
app.register_blueprint(t_autorizzazioni_controller, url_prefix='/autorizzazioni')

if __name__ == '__main__':
    app.run(debug=True)