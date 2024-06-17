import mysql.connector

class database:

    def __init__(self):
        
        self.Con = None
        self.Cur = None

    def connetti(self, hostname, dbname, username, password):

        self.Host = hostname
        self.Db = dbname
        self.User = username
        self.Pwd = password

        try:

            conn = mysql.connector.connect(
           
                host = self.Host,
                user = self.User,
                password = self.Pwd,
                database = self.Db

            )

            self.Con = conn

        except Exception as e:

            print (e)
            self.Con = None

        #return self.Con

    def cursore(self,istruzione):

        if self.Con:
            self.Cur = self.Con.cursor(istruzione)
        else:
            self.Cur = None

        #return self.Cur

    def BeginTransaction(self):

        self.Con.start_transaction()

    def CommitTransacion(self):

        self.Con.commit()

    def RollbackTransaction(self):

        self.Con.rollback()
