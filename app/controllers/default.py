from flask import redirect, request
from flask import render_template
from flask import url_for
from flask import flash, session
from app import app
from app.models.forms import FormLogin, FormUserCreate
from app.models.forms import FormCar
from app.models.forms import Agenda
from app.models.db import DBConn
from datetime import date, timedelta



####################################### 
####################################### Dashboard
####################################### 

class Dashboard():
    def index(self):
        return render_template('index.html')


####################################### 
####################################### Auth
####################################### 

class Auth():
    def login(self):
        user = FormLogin()
        if user.validate_on_submit():
            if user.errors:
                flash('{}'.format(user.errors),'alert')
            else:
                if user.login():
                    return redirect(url_for('index'))
        return render_template('user_login.html', form_login=user)

    def logout(self):
        user = FormLogin()
        user.logout()
        return redirect(url_for('login'))



####################################### 
####################################### User
####################################### 

class User():
    def create(self):
        user = FormUserCreate()
        if user.validate_on_submit():
            if user.errors:
                flash('{}'.format(user.errors),'alert')
            elif user.password.data != user.password_confirm.data:
                flash('Senhas diferentes!','alert')
            else:
                if user.create():
                    return redirect(url_for('login'))
        return render_template('user_create.html', form_user=user )

    def edit(self,id):
        user = FormUserCreate()
        if 'username' in session:
            if user.validate_on_submit():
                if user.errors:
                    flash('{}'.format(user.errors),'alert')
                else:
                    user.update(id)
                return redirect(url_for('users_manager'))
            else:
                user.read(id)
                return render_template('user_create.html', form_user=user)
        else:
            return redirect(url_for('index'))


    def manager(self):
        user = FormUserCreate()
        if 'username' in session:
            if session['admin'] == True:
                users = user.get_all()
            else:
                users = user.get_one(session['id'])
            return render_template('users_manager.html', users=users )
        else:
            return redirect(url_for('index'))


    def manager_delete(self,id):
        user = FormUserCreate()
        if 'username' in session:
            if session['admin'] == True and session['id'] != id:
                user.delete(id)
            else:
                flash('Operação não permitida!','alert')
        else:
            flash('Usuário não logado!','alert')
        return redirect(url_for('users_manager'))


####################################### 
####################################### Car
####################################### 
class Car():
    def cars_manager(self):
        if 'username' in session:
            car = FormCar()
            if 'car_edit_id' in session:
                car.select( session['car_edit_id'] )

            if car.validate_on_submit():
                if car.errors:
                    flash('{}'.format(car.errors),'alert')
                else:
                    if 'car_edit_id' in session:
                        car.update(session['car_edit_id'])
                        session.pop('car_edit_id', None)
                        return redirect( url_for('cars_manager'))
                    else:
                        if car.is_valid():
                            car.insert()
                        else:
                            flash('Carrinho já existe!','alert')
                        return redirect( url_for('cars_manager'))
            car_list=car.list_all()
            return render_template('cars_manager.html', form_car=car, cars=car_list )
        else:
            return redirect( url_for('index'))

    def cars_delete(self,id):
        if 'username' in session:
            if session['admin'] == True:
                car = FormCar()
                car.delete(id)
        return redirect(url_for('cars_manager'))

    def cars_edit(self,id):
        if 'username' in session:
            if session['admin'] == True:
                session['car_edit_id'] = id
        return redirect(url_for('cars_manager'))



####################################### 
####################################### Reservations
####################################### 

class Reserv():
    def reserves(self):
        agenda = Agenda()
        session['today_date'] = date.today()
        if not 'reservation_date' in session:
            session['reservation_date'] = date.today()
        if request.method == 'POST':
            session['reservation_date'] = request.form['calendario']
        lst = agenda.lst()
        return render_template('reservations.html', lst=lst )

    def scheduling(self):
        agenda = Agenda()
        session['today_date'] = date.today()
        session['max_date'] = date.today() + timedelta(days=30)
        if not 'reservation_date' in session:
            session['reservation_date'] = date.today()
        if request.method == 'POST':
            session['reservation_date'] = request.form['calendario']
        lst = agenda.lst()
        return render_template('scheduling.html', lst=lst )

    def scheduling_cancel(self, car, periodo):
        if 'username' in session:
            db = DBConn()
            id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
            if id is not None:
                if   periodo == 2: #'m':
                    db.sql_cmd("UPDATE reservations SET user_m=NULL WHERE id='{}';".format(id[0][0]) )
                elif periodo == 3: #'t':
                    db.sql_cmd("UPDATE reservations SET user_t=NULL WHERE id='{}';".format(id[0][0]) )
                elif periodo == 4: #'n':
                    db.sql_cmd("UPDATE reservations SET user_n=NULL WHERE id='{}';".format(id[0][0]) )
        return redirect(url_for('scheduling'))

    def scheduling_reserve(self, car, periodo):
        if 'username' in session:
            db = DBConn()
            id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
            if id:
                if periodo == 2: # 'm'
                    db.sql_cmd("UPDATE reservations SET user_m='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
                elif periodo == 3: #'t':
                    db.sql_cmd("UPDATE reservations SET user_t='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
                elif periodo == 4: #'n':
                    db.sql_cmd("UPDATE reservations SET user_n='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
            else:
                if   periodo == 2: #'m':
                    db.sql_cmd("INSERT INTO reservations (res_date, car, user_m) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
                elif periodo ==  3: #'t':
                    db.sql_cmd("INSERT INTO reservations (res_date, car, user_t) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
                elif periodo == 4: # 'n':
                    db.sql_cmd("INSERT INTO reservations (res_date, car, user_n) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
        return redirect(url_for('scheduling'))



####################################### 
####################################### Instanciamento
####################################### 


dashboard = Dashboard()
auth = Auth()
user = User()
car = Car()
agenda = Reserv()



####################################### 
####################################### 
####################################### 

@app.route("/")
def index():
    return dashboard.index()

@app.route("/user_login", methods=['GET','POST'])
def login():
    return auth.login()

@app.route("/user_logout")
def logout():
    return auth.logout()




@app.route("/create_user", methods=['GET','POST'])
def create_user():
    return user.create()

@app.route("/delete_user/<int:id>")
def users_delete(id):
    return user.manager_delete(id)

@app.route("/edit_user/<int:id>", methods=['GET', 'POST'])
def users_edit(id):
    return user.edit(id)

@app.route("/users_manager", methods=['GET','POST'])
def users_manager():
    return user.manager()




@app.route("/cars_manager", methods=['GET','POST'])
def cars_manager():
    return car.cars_manager()

@app.route("/delete_car/<int:id>")
def cars_delete(id):
    return car.cars_delete(id)

@app.route("/edit_car/<int:id>")
def cars_edit(id):
    return car.cars_edit(id)



@app.route('/reservations', methods=['GET','POST'])
def reservations():
    return agenda.reserves()

@app.route('/scheduling', methods=['GET','POST'])
def scheduling():
    return agenda.scheduling()

@app.route('/scheduling/cancel/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_cancel(car, periodo):
    return agenda.scheduling_cancel(car, periodo)

@app.route('/scheduling/reservar/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_reservar(car, periodo):
    return agenda.scheduling_reserve(car,periodo)




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

    db = DBConn()
    db.create_db()
    return redirect( url_for('index'))



@app.route("/test")
def test():
    return render_template('test.html')