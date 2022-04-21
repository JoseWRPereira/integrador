from flask import redirect, request
from flask import render_template
from flask import url_for
from flask import flash
from app import app
from app.models.forms import LoginForm, NewUserForm
from app.models.db import DBConn

db = DBConn()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET','POST'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        print(form_login.email.data)
        print(form_login.password.data)
        if form_login.errors:
            print(form_login.errors)
            flash('{}'.format(form_login.errors),'alert')
    return render_template('login.html', form_login=form_login)


@app.route("/newuser", methods=['GET','POST'])
def newuser():
    form_newuser = NewUserForm()
    if form_newuser.validate_on_submit():
        if form_newuser.errors:
            flash('{}'.format(form_newuser.errors),'alert')
        elif form_newuser.password.data != form_newuser.password_confirm.data:
            flash('Senhas diferentes!','alert')
        else:
            db = DBConn()
            db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( form_newuser.name.data, form_newuser.email.data, form_newuser.password.data ) )
            return( redirect( url_for('users')) )
    return render_template('newuser.html', form_newuser=form_newuser)


@app.route("/users")
def users():
    db = DBConn()
    users = db.sql_fetch("SELECT * FROM users;")
    return render_template('users.html', users=users)




@app.route("/dbreset")
def dbreset():
    db.credential_defaul(  dbname='db_integrador')
    db.sql_cmd("DROP TABLE IF EXISTS users;")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10) );")
    db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( "Admin","admin@email.com", "admin" ) )
    users = db.sql_fetch("SELECT * FROM users;")
    for u in users:
        print( u[0] )
    return( redirect( url_for('users')) )


