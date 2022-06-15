FLASK_APP = 'app/app.py'
FLASK_ENV = 'development'
DEBUG = True
SECRET_KEY = 'integracao'

# # Parâmetros de conexão com banco de dados Postgres no Heroku
# DB_HOST = 'ec2-3-211-6-217.compute-1.amazonaws.com'
# DB_DATABASE = 'd1r5lc2aibuqho'
# DB_USER = 'osgdqebnpjiady'
# DB_PORT = '5432'
# DB_PASSWORD = '6a41acdfce24f4c0a4b6629ec1c465bea2365ec75e07cd4d231d33c36421e75a'
# DB_URI = "postgres://osgdqebnpjiady:6a41acdfce24f4c0a4b6629ec1c465bea2365ec75e07cd4d231d33c36421e75a@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d1r5lc2aibuqho"

# Parâmetros de conexão com banco de dados Postgres local
DB_HOST = '127.0.0.1'
DB_DATABASE = 'db_integrador'
DB_USER = 'postgres'
DB_PORT = '5432'
DB_PASSWORD = 'postgres'
DB_URI = "postgresql://postgres:postgres@localhost:5432/db_integrador"
