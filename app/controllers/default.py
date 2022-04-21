from flask import redirect, request
from flask import render_template
from flask import url_for
from flask import flash
from app import app
from app.models.forms import LoginForm
from app.models.db import DBConn


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        print(form_login.username.data)
        print(form_login.password.data)
        if form_login.errors:
            print(form_login.errors)
            flash('{}'.format(form_login.errors),'alert')
    return render_template('login.html', form_login=form_login)

@app.route("/logins", methods=['GET','POST'])
def logins():
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['senha']
        if user == 'admin@email.com' and password == 'admin':
            # return redirect( url_for('index'))
            return "OK"
        else:
            flash('Login incorreto! Tente outra vez...','alert')
            return redirect( url_for('login'))
    else:
        return render_template('login.html')

@app.route("/newuser", methods=['GET','POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['nome']
        email = request.form['email']
        password = request.form['passwd']
        confirm = request.form['confirm']
        if password == confirm:
            # return redirect( url_for('index'))
            return "OK"
        else:
            flash('Senhas diferentes!','alert')
            return redirect( url_for('newuser'))
    else:
        return render_template('newuser.html')




@app.route("/dbreset")
def dbreset():
    db = DBConn()
    db.credential_defaul(  dbname='db_integrador')

    db.sql_cmd("DROP TABLE IF EXISTS users;")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10) );")
    db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( "Admin","admin@email.com", "admin" ) )
    
    return( redirect( url_for('newuser')) )