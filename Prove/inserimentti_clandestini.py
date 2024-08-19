# import pyodbc
# import pandas as pd
# from sqlalchemy import create_engine
# import mysql.connector

# # 1. Connessione a SQL Server
# server = r'NBW009\SQLEXPRESS'
# database = 'cucina'
# username = 'sa'
# password = 'michele'

# # Stringa di connessione
# sql_server_conn_str = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     f'SERVER={server};'
#     f'DATABASE={database};'
#     f'UID={username};'
#     f'PWD={password}'
# )

# # Connessione a SQL Server
# sql_server_conn = pyodbc.connect(sql_server_conn_str)

# # 2. Esportare i dati da SQL Server
# # query_conservazione = "SELECT [id], [nome] FROM [Cucina2].[dbo].[t_tipologiaConservazione]"
# # df_conservazione = pd.read_sql(query_conservazione, sql_server_conn)

# query_ordini = "SELECT id, fkReparto, [fkScheda] FROM [Cucina].[dbo].[t_ordiniSchede]"
# df_ordini = pd.read_sql(query_ordini, sql_server_conn)

# sql_server_conn.close()

# # 3. Creare le tabelle in MySQL
# mysql_conn = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="Mulini24!",
#     database="cucina"
# )

# # Creazione della tabella t_tipologiaConservazione in MySQL
# # create_table_conservazione_query = """
# # CREATE TABLE IF NOT EXISTS t_tipologiaConservazione (
# #     id INT PRIMARY KEY,
# #     nome VARCHAR(255)
# # );
# # """
# cursor = mysql_conn.cursor()
# # cursor.execute(create_table_conservazione_query)
# # mysql_conn.commit()

# # Creazione della tabella t_tipologiaAlimenti in MySQL
# # create_table_alimenti_query = """
# # CREATE TABLE IF NOT EXISTS t_tipologiaAlimenti (
# #     id INT PRIMARY KEY,
# #     nome VARCHAR(255),
# #     fktipologiaConservazione INT,
# #     FOREIGN KEY (fktipologiaConservazione) REFERENCES t_tipologiaConservazione(id)
# # );
# # """
# # cursor.execute(create_table_alimenti_query)
# mysql_conn.commit()

# # 4. Importare i dati in MySQL
# mysql_user = 'root'
# mysql_password = 'Mulini24!'
# mysql_host = '127.0.0.1'
# mysql_database = 'cucina'

# engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

# # Importare i dati nella tabella t_tipologiaConservazione
# # df_conservazione.to_sql('t_tipologiaConservazione', engine, if_exists='append', index=False)

# # Importare i dati nella tabella t_tipologiaAlimenti
# df_alimenti.to_sql('t_tipologiaAlimenti', engine, if_exists='append', index=False)

# # Chiudere la connessione
# mysql_conn.close()

# print("Dati trasferiti con successo!")
