import pyodbc
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# 1. Connessione a SQL Server
server = r'NBW009\SQLEXPRESS'
database = 'cucina'
username = 'sa'
password = 'michele'

# Stringa di connessione
sql_server_conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

try:
    # Connessione a SQL Server
    sql_server_conn = pyodbc.connect(sql_server_conn_str)

    # 2. Esportare i dati da SQL Server
    query = """
    SELECT id, fkReparto, [fkScheda] FROM [Cucina].[dbo].[t_ordiniSchede]
    """
    df = pd.read_sql(query, sql_server_conn)
    
finally:
    # Chiudere la connessione SQL Server
    sql_server_conn.close()

# 3. Connessione a MySQL
mysql_conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Mulini24!",
    database="cucina"
)

cursor = mysql_conn.cursor()

# 4. Costruire e eseguire le query di aggiornamento
update_queries = []
for index, row in df.iterrows():
    query = f"""
    UPDATE cucina.t_ordinischede
    SET fkScheda = {row['fkScheda']}
    WHERE id = {row['id']} AND fkReparto = {row['fkReparto']};
    """
    update_queries.append(query)

# Eseguire le query di aggiornamento
try:
    for query in update_queries:
        cursor.execute(query)
    mysql_conn.commit()
    print("Dati aggiornati con successo!")
except Exception as e:
    print(f"Errore durante l'aggiornamento dei dati: {e}")
    mysql_conn.rollback()
finally:
    # Chiudere la connessione MySQL
    cursor.close()
    mysql_conn.close()
