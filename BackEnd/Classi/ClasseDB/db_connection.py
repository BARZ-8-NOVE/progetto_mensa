import mysql.connector
from mysql.connector import Error
from Classi.ClasseDB.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class Database:
    def __init__(self):
        self.Connection = None

    def create_connection(self):
        """Create a database connection."""
        try:
            self.Connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                use_pure=True  # Utilizza TCP/IP
            )
            if self.Connection.is_connected():
                print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
            raise Exception

    def close_connection(self):
        """Close a database connection."""
        if self.Connection and self.Connection.is_connected():
            self.Connection.close()
            print("The connection is closed")

    def execute_query(self, query, params=None):
        """Execute a query on the database."""
        cursor = self.Connection.cursor()
        try:
            cursor.execute(query, params)
            self.Connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        return cursor

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def create_cursor(self):
        """Create a cursor"""
        if self.Connection:
            self.Cursor = self.Connection.cursor()
            return self.Cursor
        else:
            self.Connection = None
            self.Cursor = None
            raise Exception
        
    def begin_transaction(self):
        """Begin a Transaction"""
        if self.Connection:
            if not self.Connection.in_transaction:
                self.Connection.start_transaction()
        else:
            self.Connection = None
            raise Exception
    
    def commit_transaction(self):
        """Commit a transaction"""
        if self.Connection:
            if self.Connection.in_transaction:
                self.Connection.commit()
        else:
            self.Connection = None
            raise Exception

    def rollback_transaction(self):
        """Rollback a transaction"""
        if self.Connection:
            if self.Connection.in_transaction:
                self.Connection.rollback()
        else:
            self.Connection = None
            raise Exception