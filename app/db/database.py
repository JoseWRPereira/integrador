from flask import Blueprint, redirect, url_for
from app.db.dbcon import DBConn

database_bp = Blueprint('database_bp', __name__)

@database_bp.route('/database_reset', methods=['GET'])
def database_reset():
    db = DBConn()
    db.sql_cmd("DROP TABLE IF EXISTS users;")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10), nif VARCHAR(10), admin BOOLEAN );")
    db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('Administrador','admin@email.com','admin','0000',True);" )
    return redirect(url_for('index'))

@database_bp.route('/list_users', methods=['GET'])
def list_users():
    db = DBConn()
    lst = db.sql_fetch("SELECT * FROM users;")
    return "{}".format(lst)


