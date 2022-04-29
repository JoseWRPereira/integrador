import psycopg2
import psycopg2.extras
from psycopg2 import Error

class DBConn():
    def __init__(self):
        self.host = '127.0.0.1'
        self.database = 'db_integrador'
        self.user = 'postgres'
        self.port = '5432'
        self.password = 'postgres'
        self.uri = "postgresql://postgres:postgres@localhost:5432/db_integrador"
    
        # self.host = 'ec2-3-211-6-217.compute-1.amazonaws.com'
        # self.database = 'd1r5lc2aibuqho'
        # self.user = 'osgdqebnpjiady'
        # self.port = '5432'
        # self.password = '6a41acdfce24f4c0a4b6629ec1c465bea2365ec75e07cd4d231d33c36421e75a'
        # self.uri = "postgres://osgdqebnpjiady:6a41acdfce24f4c0a4b6629ec1c465bea2365ec75e07cd4d231d33c36421e75a@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d1r5lc2aibuqho"

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


    def create_db(self):
        self.sql_cmd("DROP TABLE IF EXISTS reservations;")
        self.sql_cmd("DROP TABLE IF EXISTS cars;")
        self.sql_cmd("DROP TABLE IF EXISTS users;")
        self.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10), nif VARCHAR(10), admin BOOLEAN );")
        self.sql_cmd("CREATE TABLE IF NOT EXISTS cars ( id SERIAL PRIMARY KEY, name VARCHAR(20) );")
        self.sql_cmd("CREATE TABLE IF NOT EXISTS reservations (id SERIAL PRIMARY KEY, res_date DATE, car INTEGER, user_m INTEGER, user_t INTEGER, user_n INTEGER);")
        self.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('Administrador','admin@email.com','admin','0000',True);" )
