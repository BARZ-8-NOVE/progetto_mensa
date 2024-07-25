import pandas as pd

# Leggi i file CSV
df_original = pd.read_csv('Prove/tutti_i_piatti_fkpiatto_giusto.csv', delimiter=';')
df_new_assoc = pd.read_csv('Prove/associazione_piatti.csv')

# Rinomina le colonne per facilitare il merging
df_new_assoc.columns = ['id', 'fkPiatto', 'fkPreparazione', 'dataInserimento', 'utenteInserimento', 'dataCancellazione', 'utenteCancellazione']

# Merge dei due DataFrame basato su fkPiatto e fkPreparazione
merged_df = pd.merge(df_original, df_new_assoc, on=['fkPiatto', 'fkPreparazione'], suffixes=('', '_assoc'))

# Seleziona le colonne richieste e rinomina
final_df = merged_df[['fkMenuServizio', 'id_assoc', 'dataInserimento_assoc', 'utenteInserimento_assoc', 'dataCancellazione_assoc', 'utenteCancellazione_assoc']]
final_df.columns = ['fkMenuServizio', 'fkAssociazione', 'dataInserimento', 'utenteInserimento', 'dataCancellazione', 'utenteCancellazione']

# Salva il nuovo CSV
final_df.to_csv('Prove/output.csv', index=False)

print("Nuovo file CSV creato con successo!")
