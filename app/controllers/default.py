from crypt import methods
from flask import redirect
from flask import render_template
from flask import url_for
from flask import flash, session
from app import app
from app.models.forms import LoginForm, NewUserForm, User
from app.models.db import DBConn
from app.models.forms import User


db = DBConn()
usr = User()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET','POST'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        if form_login.errors:
            flash('{}'.format(form_login.errors),'alert')
        else:
            if usr.login_validate(form_login.email.data, form_login.password.data):
                return render_template('index.html')
    return render_template('login.html', form_login=form_login)


@app.route("/logoff", methods=['GET'])
def logoff():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for('login'))


@app.route("/newuser", methods=['GET','POST'])
def newuser():
    form_newuser = NewUserForm()
    if form_newuser.validate_on_submit():
        if form_newuser.errors:
            flash('{}'.format(form_newuser.errors),'alert')
        elif form_newuser.password.data != form_newuser.password_confirm.data:
            flash('Senhas diferentes!','alert')
        else:
            if usr.newuser_validate(form_newuser.name.data, form_newuser.email.data, form_newuser.password.data):
                return render_template(url_for(users))
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


