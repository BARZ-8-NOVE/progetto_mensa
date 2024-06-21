import sys
import os
from flask import Flask

# Aggiungi la directory di progetto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Classi.ClasseDB.db_connection import Database
from Classi.ClasseUtenti.ClasseUtenti import t_utenti
from Classi.ClasseAlimenti.Classe_t_alimenti import t_alimenti

progetto_mensa = Flask(__name__)

@progetto_mensa.route('/get_t_alimenti', methods = ['GET'])
def get_t_alimenti():
    alimenti = t_alimenti()
    return alimenti.get_t_alimenti_by_id()

def fetch_data_prova_connessione():
    db = Database()
    db.create_connection()
    if db.Connection:
        query = "SELECT * FROM cucina.t_alimenti"  
        rows = db.fetch_all(query)
        for row in rows:
            print(row)
        db.close_connection()

if __name__ == "__main__":
    progetto_mensa.run('0.0.0.0', port = 81, debug = True)
    #fetch_data_prova_connessione()