import pandas as pd

# Percorso del file CSV
file_path = 'DBMS/file_dati_statici/t_preparazionicontenuti.csv'

# Leggi il CSV in un DataFrame
df = pd.read_csv(file_path)

# Trasforma tutti i valori nulli o 0 nella colonna quantita in 0.1
df['quantita'] = df['quantita'].fillna(0.1).replace(0, 0.1)

# Sovrascrivi il file CSV con le righe aggiornate
df.to_csv(file_path, index=False)

print(f"Trasformazione completata. Il file {file_path} è stato aggiornato con i valori di quantita modificati.")
