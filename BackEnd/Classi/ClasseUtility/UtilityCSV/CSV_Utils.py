import pandas as pd
from sqlalchemy.orm import Session

def populate_from_csv_with_ids(session: Session, model, csv_file_path: str):
    """
    Popola una tabella da un file CSV se la tabella è vuota.
    
    :param session: La sessione del database.
    :param model: La classe del modello SQLAlchemy della tabella da popolare.
    :param csv_file_path: Il percorso del file CSV.
    """
    df = pd.read_csv(csv_file_path)
    data_to_insert = df.to_dict(orient='records')
    
    # Verifica se la tabella è vuota
    count = session.query(model).count()
    if count == 0:
        session.bulk_insert_mappings(model, data_to_insert)
        session.commit()
