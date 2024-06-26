from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.config import DATABASE_URI
from Classi.ClasseDB.db_connection import get_db, Base, engine
from Classi.ClasseAlimenti.Classe_t_alimenti import TAlimenti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = engine

@app.route('/alimenti/<int:id>', methods=['GET'])
def get_alimenti(id):
    session = sessionmaker(bind=db)()
    t_alimenti_instance = TAlimenti()  # Creare un'istanza di TAlimenti
    response = t_alimenti_instance.get_t_alimenti_by_id(session, id)  # Chiamare il metodo sull'istanza
    session.close()  # Chiudi la sessione dopo l'uso
    return jsonify(response), 200 if 'Error' not in response else 404

if __name__ == '__main__':
    app.run(debug=True)