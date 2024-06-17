import mysql.connector
from mysql.connector import Error
from InfoDB.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class Database:
    def __init__(self):
        self.connection = None

    def create_connection(self):
        """Create a database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                use_pure=True  # Utilizza TCP/IP
            )
            if self.connection.is_connected():
                print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        """Close a database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("The connection is closed")

    def execute_query(self, query, params=None):
        """Execute a query on the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        return cursor

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
