import psycopg2
import psycopg2.extras
from psycopg2 import Error
from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_URI, DB_USER

class DBConn():
    def __init__(self):
        self.host = DB_HOST
        self.database = DB_DATABASE
        self.user = DB_USER
        self.port = DB_PORT
        self.password = DB_PASSWORD
        self.uri = DB_URI


    def sql_fetch(self, sql):
        try:
            connection = psycopg2.connect( self.uri )
            cursor = connection.cursor()
            cursor.execute(sql)
            print("SQL FETCH: ", sql, "\n")
            lista = cursor.fetchall()
            for l in lista:
                print("  ", l, "\n")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
            cursor.execute("ROLLBACK;")
            lista = []
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                return lista


    def sql_cmd(self, sql):
        try:
            connection = psycopg2.connect(  database=self.database,
                                            user=self.user,
                                            password=self.password,
                                            host=self.host,
                                            port=self.port
                                        )
            cursor = connection.cursor()
            cursor.execute(sql)
            print("SQL CMD: ", sql, "\n")
            cursor.execute("COMMIT;")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL: ", error)
            cursor.execute("ROLLBACK;")
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
