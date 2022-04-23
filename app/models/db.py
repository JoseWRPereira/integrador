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
    
    def credential_defaul(self, dbname):
        self.database = dbname
        # self.uri = "postgresql://"+self.user+":"+self.password+"@"+self.host+":"+self.port+"/"+self.database
        self.uri = "postgresql://postgres:postgres@localhost:5432/db_integrador"

    def credential(self, host, dbname, user, port, passwd):
        self.host = host
        self.database = dbname
        self.user = user
        self.port = port
        self.password = passwd
        self.uri = "postgresql://"+user+":"+passwd+"@"+host+":"+port+"/"+dbname


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


# class DBCredential_local:
#     def __init__(self):
#         self.host = '127.0.0.1'
#         self.database = 'db_integrador'
#         self.user = 'postgres'
#         self.port = '5432'
#         self.password = 'postgres'
#         self.uri = "postgresql://postgres:postgres@localhost:5432/db_integrador"

# class DBCredential_online:
#     def __init__(self):
#         self.host = 'ec2-52-20-143-167.compute-1.amazonaws.com'
#         self.database = 'd1f1r9u6nff5vk'
#         self.user = 'kgjlgrirpawegc'
#         self.port = '5432'
#         self.password = 'b6e2ce9c166a323946076f92d4cf13911b342f777555a391e7cc599208f83b39'
#         self.uri = 'postgres://kgjlgrirpawegc:b6e2ce9c166a323946076f92d4cf13911b342f777555a391e7cc599208f83b39@ec2-52-20-143-167.compute-1.amazonaws.com:5432/d1f1r9u6nff5vk'
#         self.heroku_cli = 'heroku pg:psql postgresql-octagonal-47192 --app agendei-pi1'


