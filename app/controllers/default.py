from flask import redirect, request
from flask import render_template
from flask import url_for
from flask import flash, session
from app import app
from app.models.forms import LoginForm, NewUserForm, EditUserForm, User
from app.models.forms import CarForm
from app.models.forms import Agenda
from app.models.db import DBConn
from datetime import date, timedelta

db = DBConn()
usr = User()
agenda = Agenda()

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


@app.route("/logoff")
def logoff():
    usr.logout()
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
            if usr.newuser_validate(form_newuser.name.data, form_newuser.email.data, form_newuser.password.data, form_newuser.nif.data):
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
    users = db.sql_fetch("SELECT id,name,email,nif,admin FROM users;")
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




@app.route('/reservations', methods=['GET','POST'])
def reservations():
    session['today_date'] = date.today()
    if not 'reservation_date' in session:
        session['reservation_date'] = date.today()
    if request.method == 'POST':
        session['reservation_date'] = request.form['calendario']
    lst = agenda.lst()
    return render_template('reservations.html', lst=lst )




@app.route('/scheduling', methods=['GET','POST'])
def scheduling():
    session['today_date'] = date.today()
    session['max_date'] = date.today() + timedelta(days=30)
    print(session['today_date'])
    if not 'reservation_date' in session:
        session['reservation_date'] = date.today()
    if request.method == 'POST':
        session['reservation_date'] = request.form['calendario']
    lst = agenda.lst()
    return render_template('scheduling.html', lst=lst )


@app.route('/scheduling/cancel/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_cancel(car, periodo):
    if 'username' in session:
        id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
        if id is not None:
            if   periodo== 1: #'m':
                db.sql_cmd("UPDATE reservations SET user_m=NULL WHERE id='{}';".format(id[0][0]) )
            elif periodo == 2: #'t':
                db.sql_cmd("UPDATE reservations SET user_t=NULL WHERE id='{}';".format(id[0][0]) )
            elif periodo == 3: #'n':
                db.sql_cmd("UPDATE reservations SET user_n=NULL WHERE id='{}';".format(id[0][0]) )
    return redirect(url_for('scheduling'))


@app.route('/scheduling/reservar/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_reservar(car, periodo):
    if 'username' in session:
        id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
        if id:
            if periodo == 1: # 'm'
                db.sql_cmd("UPDATE reservations SET user_m='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
            elif periodo == 2: #'t':
                db.sql_cmd("UPDATE reservations SET user_t='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
            elif periodo == 3: #'n':
                db.sql_cmd("UPDATE reservations SET user_n='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
        else:
            if   periodo == 1: #'m':
                db.sql_cmd("INSERT INTO reservations (res_date, car, user_m) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
            elif periodo ==  2: #'t':
                db.sql_cmd("INSERT INTO reservations (res_date, car, user_t) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
            elif periodo == 3: # 'n':
                db.sql_cmd("INSERT INTO reservations (res_date, car, user_n) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
    return redirect(url_for('scheduling'))






@app.route("/dbreset")
def dbreset():

    if 'username' in session:
        session.pop('username', None)
    if 'email' in session:
        session.pop('email', None)
    if 'id' in session:
        session.pop('id', None)
    if 'nif' in session:
        session.pop('nif', None)
    if 'admin' in session:
        session.pop('admin', None)


    # db.credential_defaul(  dbname='db_integrador')
    db.sql_cmd("DROP TABLE IF EXISTS reservations;")
    db.sql_cmd("DROP TABLE IF EXISTS cars;")
    db.sql_cmd("DROP TABLE IF EXISTS users;")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), password VARCHAR(10), nif VARCHAR(10), admin BOOLEAN );")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS cars ( id SERIAL PRIMARY KEY, name VARCHAR(20) );")
    db.sql_cmd("CREATE TABLE IF NOT EXISTS reservations (id SERIAL PRIMARY KEY, res_date DATE, car INTEGER, user_m INTEGER, user_t INTEGER, user_n INTEGER);")
    db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('Administrador','admin@email.com','admin','0000',True);" )
    # db.sql_cmd("INSERT INTO reservations (res_date,car,user_m,user_t,user_n) VALUES ('{}','{}','{}','{}','{}');".format('2022-04-24', 1, 1, 2, 3))
    # db.sql_cmd("INSERT INTO reservations (res_date,car,user_m,user_t) VALUES ('{}','{}','{}','{}');".format('2022-04-25', 1, 2, 3))
    # db.sql_cmd("INSERT INTO reservations (res_date,car,user_m) VALUES ('{}','{}','{}');".format('2022-04-25', 2, 1))
    # db.sql_cmd("INSERT INTO reservations (res_date,car,user_m) VALUES ('{}','{}','{}');".format('2022-04-25', 3, 4))
    # db.sql_cmd("INSERT INTO reservations (res_date,car,user_m,user_t,user_n) VALUES ('{}','{}','{}','{}','{}');".format('2022-04-26', 2, 1, 2, 1))
    return redirect( url_for('index'))

