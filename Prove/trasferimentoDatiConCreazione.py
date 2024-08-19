import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

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
        SELECT [id]
            ,[fkOrdineScheda]
            ,[fkPiatto]
            ,[quantita]
            ,[note]
        FROM [Cucina].[dbo].[t_ordiniSchedePiatti]
        WHERE fkPiatto IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 45, 47, 48, 58, 60, 65, 66, 72, 73, 75, 78, 81, 83, 85, 87);
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

# Creare la tabella in MySQL
create_table_query = """
CREATE TABLE IF NOT EXISTS t_ordiniSchedePiatti (
    id INT PRIMARY KEY,
    fkOrdineScheda INT,
    fkPiatto INT,
    quantita INT,
    note VARCHAR(255),
    FOREIGN KEY (fkOrdineScheda) REFERENCES t_ordinischede(id),
    FOREIGN KEY (fkPiatto) REFERENCES t_piatti(id)
);
"""
cursor.execute(create_table_query)
mysql_conn.commit()

# 4. Importare i dati in MySQL
mysql_user = 'root'
mysql_password = 'Mulini24!'
mysql_host = '127.0.0.1'
mysql_database = 'cucina'

engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

try:
    df.to_sql('t_ordiniSchedePiatti', engine, if_exists='append', index=False)
    print("Dati trasferiti con successo!")
except Exception as e:
    print(f"Errore durante il trasferimento dei dati: {e}")
finally:
    # Chiudere la connessione MySQL
    mysql_conn.close()
