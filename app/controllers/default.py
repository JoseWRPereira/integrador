from flask import redirect, request
from flask import render_template
from flask import url_for
from flask import flash, session
from app import app
from app.models.forms import LoginForm, NewUserForm, EditUserForm, User
from app.models.forms import CarForm
from app.models.db import DBConn


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
                return redirect(url_for('login'))
    return render_template('newuser.html', form_newuser=form_newuser)


@app.route("/users/delete/<int:id>")
def users_delete(id):
    if 'username' in session:
        db.sql_cmd("DELETE FROM users WHERE id='{}';".format(id) )
    return redirect(url_for('users_manager'))


@app.route("/users/edit/<int:id>", methods=['GET', 'POST'])
def users_edit(id):
    if 'username' in session:
        form_edituser = EditUserForm()
        if request.method == 'POST':
            form_edituser.saveUser(id)
            return redirect(url_for('users_manager'))
        else:
            form_edituser.selectUser(id)
    return render_template('edituser.html', form_edituser=form_edituser)


@app.route("/users/manager", methods=['GET','POST'])
def users_manager():
    db = DBConn()
    users = db.sql_fetch("SELECT id, name, email FROM users;")
    return render_template('users_manager.html', users=users)




@app.route("/cars/manager", methods=['GET','POST'])
def cars_manager():
    if 'username' in session:
        form_car = CarForm()
        if 'car_edit_id' in session:
            form_car.select( session['car_edit_id'] )

        if form_car.validate_on_submit():
            if form_car.errors:
                flash('{}'.format(form_car.errors),'alert')
            else:
                if 'car_edit_id' in session:
                    form_car.update(session['car_edit_id'])
                    session.pop('car_edit_id', None)
                    return redirect( url_for('cars_manager'))
                else:
                    if form_car.is_valid():
                        form_car.insert()
                        return redirect(url_for('cars_insert'))
                    else:
                        flash('Carrinho já existe!','alert')
                        return redirect( url_for('cars_manager'))
        cars=form_car.list_all()
        return render_template('cars_manager.html', form_car=form_car, cars=cars )
    else:
        return redirect( url_for('index'))


@app.route("/cars/insert")
def cars_insert():
    return redirect(url_for('cars_manager'))


@app.route("/cars/delete/<int:id>")
def cars_delete(id):
    if 'username' in session:
        form_car = CarForm()
        form_car.delete(id)
    return redirect(url_for('cars_manager'))


@app.route("/cars/edit/<int:id>")
def cars_edit(id):
    if 'username' in session:
        session['car_edit_id'] = id
    return redirect(url_for('cars_manager'))







@app.route("/dbreset")
def dbreset():
    db.credential_defaul(  dbname='db_integrador')
    db.sql_cmd("DROP TABLE IF EXISTS cars;")
    db.sql_cmd("DROP TABLE IF EXISTS users;")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10) );")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS cars ( id SERIAL PRIMARY KEY, name VARCHAR(20) );")
    db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( "Admin","admin@email.com", "admin" ) )
    return redirect( url_for('index'))

