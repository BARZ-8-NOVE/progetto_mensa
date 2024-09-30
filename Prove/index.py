import pandas as pd

def remove_rows_from_csv(input_csv, output_csv, names_to_remove):
    # Carica il file CSV in un DataFrame
    df = pd.read_csv(input_csv)

    # Rimuovi le righe in cui la colonna 'username' è presente in names_to_remove
    df_filtered = df[~df['username'].isin(names_to_remove)]

    # Salva il DataFrame filtrato nel nuovo file CSV
    df_filtered.to_csv(output_csv, index=False)

# Esempio di utilizzo
input_csv_path = 'C://Users//micheleb//Desktop//progetto_Cucina//progetto_mensa//new_users.csv'  # Sostituisci con il percorso del tuo file CSV di input
new_csv_path = 'users_rimossi_uno.csv' # Sostituisci con il percorso del file CSV di output

# Lista di nomi da rimuovere
names_to_remove = [
    'g.saffioti', 'm.cannarozzo', 'e.governa', 'm.crea', 's.diberti', 'v.giurdanella',
    'l.bongiovanni', 'e.pregnolato', 'g.diana', 'm.borgomastro', 'c.barile', 'f.gallo',
    'f.tuninetti', 'a.pusceddu', 's.crepaldi', 'c.savoca', 'i.capizzi', 'a.carstean',
    'g.antiquario', 'p.caodaglio', 'd.macario', 'm.carlino', 'adm.g.logozzo',
    'adm.r.verquera', 't.busana', 'f.amato', 'r.orsini', 't.monge', 'r.baldi', 
    'm.cannizzo', 'p.ruscitti', 'd.almanza', 'a.cascina', 'm.corbo', 'a.frisina', 
    'g.marletta', 'c.peragine', 's.raimondi', 'f.talerico', 'c.parrella', 
    'm.saraco', 'c.denicolai', 'l.doro', 'e.feraru', 'l.modugno', 's.neirotti', 
    'w.nuovo', 'r.vacchelli', 's.vettori', 'a.versaci', 'a.cali', 'g.cammarieri', 
    's.drogo', 'u.malis', 'd.onica', 'm.papagni', 'f.rostagno', 'r.picco', 
    'g.tedino', 'l.anfossi', 'fr.capano', 'v.latona', 'e.spitale', 'm.sanna', 
    'v.surgo', 'm.basile', 'c.ferrero', 'c.dimatteo', 'p.fornace', 'm.arangino', 
    'c.cazzato', 'a.cristofor', 'm.dangelo', 's.haghiac', 's.mastrogiovanni', 
    'm.prete', 'l.senevigo', 's.cappello', 'm.damico', 'l.belmondo', 
    'n.bonavota', 'm.borghini', 'm.brunello', 'v.burungiu', 's.fantino', 
    'g.greco', 'm.mosca', 'g.piranio', 'a.schillaci', 's.caspanello', 
    'i.caiazza', 'r.cassano', 'm.falotico', 'r.gaiola', 'g.giarmoleo', 
    'a.lopedote', 'e.pandolfo', 'g.pavese'
]

remove_rows_from_csv(input_csv_path, new_csv_path, names_to_remove)
