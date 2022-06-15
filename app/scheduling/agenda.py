from flask import Blueprint, redirect, render_template, url_for
from flask import request
from flask import flash, session
from datetime import date, timedelta
from app.db.dbcon import DBConn


agenda_bp = Blueprint('agenda_bp', __name__, template_folder='templates')


class Agenda():
    def lst(self):
        db = DBConn()
        registros = db.sql_fetch("SELECT id,name FROM cars;")

        mask = ['','m','t','n']
        lst = []
        for campo in registros:
            reg = db.sql_fetch("SELECT car,user_m,user_t,user_n FROM reservations WHERE res_date='{}' AND car='{}' ORDER BY id ASC;".format(session['reservation_date'], campo[0]) )
            sub = []
            if reg:
                for i in range(0,4):
                    if reg[0][i] != None:
                        sub.append(reg[0][i])
                        if i == 0:
                            sub.append(campo[1])
                    else:
                        sub.append(mask[i])
            else:
                sub.append(campo[0])
                sub.append(campo[1])
                sub.append(mask[1])
                sub.append(mask[2])
                sub.append(mask[3])
            lst.append(sub)
        return lst

# class Reserv():
    # def reserves(self):
    #     agenda = Agenda()
    #     session['today_date'] = date.today()
    #     if not 'reservation_date' in session:
    #         session['reservation_date'] = date.today()
    #     if request.method == 'POST':
    #         session['reservation_date'] = request.form['calendario']
    #     lst = agenda.lst()
    #     return render_template('reservations.html', lst=lst )

    # def scheduling(self):
    #     agenda = Agenda()
    #     session['today_date'] = date.today()
    #     session['max_date'] = date.today() + timedelta(days=30)
    #     if not 'reservation_date' in session:
    #         session['reservation_date'] = date.today()
    #     if request.method == 'POST':
    #         session['reservation_date'] = request.form['calendario']
    #     lst = agenda.lst()
    #     return render_template('scheduling.html', lst=lst )

    # def scheduling_cancel(self, car, periodo):
    #     if 'username' in session:
    #         db = DBConn()
    #         id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
    #         if id is not None:
    #             if   periodo == 2: #'m':
    #                 db.sql_cmd("UPDATE reservations SET user_m=NULL WHERE id='{}';".format(id[0][0]) )
    #             elif periodo == 3: #'t':
    #                 db.sql_cmd("UPDATE reservations SET user_t=NULL WHERE id='{}';".format(id[0][0]) )
    #             elif periodo == 4: #'n':
    #                 db.sql_cmd("UPDATE reservations SET user_n=NULL WHERE id='{}';".format(id[0][0]) )
    #     return redirect(url_for('scheduling'))

    # def scheduling_reserve(self, car, periodo):
    #     if 'username' in session:
    #         db = DBConn()
    #         id = db.sql_fetch("SELECT id FROM reservations WHERE res_date='{}' AND car='{}';".format(session['reservation_date'], car) )
    #         if id:
    #             if periodo == 2: # 'm'
    #                 db.sql_cmd("UPDATE reservations SET user_m='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
    #             elif periodo == 3: #'t':
    #                 db.sql_cmd("UPDATE reservations SET user_t='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
    #             elif periodo == 4: #'n':
    #                 db.sql_cmd("UPDATE reservations SET user_n='{}' WHERE id='{}';".format(session['id'], id[0][0]) )
    #         else:
    #             if   periodo == 2: #'m':
    #                 db.sql_cmd("INSERT INTO reservations (res_date, car, user_m) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
    #             elif periodo ==  3: #'t':
    #                 db.sql_cmd("INSERT INTO reservations (res_date, car, user_t) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
    #             elif periodo == 4: # 'n':
    #                 db.sql_cmd("INSERT INTO reservations (res_date, car, user_n) VALUES ('{}','{}','{}');".format(session['reservation_date'], car, session['id']) )
    #     return redirect(url_for('scheduling'))





@agenda_bp.route('/reservations', methods=['GET','POST'])
def reservations():
    # return agenda.reserves()
    # def reserves(self):
    agenda = Agenda()
    session['today_date'] = date.today()
    if not 'reservation_date' in session:
        session['reservation_date'] = date.today()
    if request.method == 'POST':
        session['reservation_date'] = request.form['calendario']
    lst = agenda.lst()
    return render_template('reservations.html', lst=lst )


@agenda_bp.route('/scheduling', methods=['GET','POST'])
def scheduling():
    # return agenda.scheduling()
    # def scheduling(self):
    agenda = Agenda()
    session['today_date'] = date.today()
    session['max_date'] = date.today() + timedelta(days=30)
    if not 'reservation_date' in session:
        session['reservation_date'] = date.today()
    if request.method == 'POST':
        session['reservation_date'] = request.form['calendario']
    lst = agenda.lst()
    return render_template('scheduling.html', lst=lst )


@agenda_bp.route('/scheduling/cancel/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_cancel(car, periodo):
    # return agenda.scheduling_cancel(car, periodo)
    # def scheduling_cancel(self, car, periodo):
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
    return redirect(url_for('agenda_bp.scheduling'))


@agenda_bp.route('/scheduling/reservar/<int:car>/<int:periodo>', methods=['GET','POST'])
def scheduling_reservar(car, periodo):
    # return agenda.scheduling_reserve(car,periodo)
    # def scheduling_reserve(self, car, periodo):
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
    return redirect(url_for('agenda_bp.scheduling'))

