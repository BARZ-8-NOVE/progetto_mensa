import sys
import os

# Aggiungi la directory di progetto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from InfoDB.db_connection import Database


def fetch_data_prova_connessione():
    db = Database()
    db.create_connection()
    if db.connection:
        query = "SELECT * FROM t_alimenti"  # Cambia 'your_table' con il nome della tua tabella
        rows = db.fetch_all(query)
        for row in rows:
            print(row)
        db.close_connection()

if __name__ == "__main__":
    fetch_data_prova_connessione()