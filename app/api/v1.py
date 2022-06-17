from flask import Blueprint
from flask import make_response, jsonify, json
from flask import render_template
from app.db.dbcon import DBConn

api_bp = Blueprint('api_bp', __name__,template_folder='templates')

@api_bp.route('/api/ajuda')
@api_bp.route('/api/help')
def api_help():
    return render_template('help.html')

@api_bp.route('/api/users')
def api_v1_users():
    db = DBConn()
    users = db.sql_fetch("SELECT id,name,email,nif,admin from users;")
    header = ["id", "name", "email", "nif", "admin"]

    dicio = []
    for user in users:
        dicio.append( dict( zip(header, user)) )

    response = make_response( jsonify(dicio), 200 )
    response.headers["Content-Type"] = "application/json"
    return response


@api_bp.route('/api/equipment')
def api_v1_equipment():
    db = DBConn()
    cars = db.sql_fetch("SELECT id,name from cars;")
    header = ["id", "name"]

    dicio = []
    for car in cars:
        dicio.append( dict( zip(header, car)) )

    response = make_response( jsonify(dicio), 200 )
    response.headers["Content-Type"] = "application/json"
    return response


@api_bp.route('/api/agenda')
def api_v1_agenda():
    db = DBConn()
    agenda = db.sql_fetch("SELECT id, res_date, car, user_m, user_t, user_n from reservations;")
    header = ["id", "res_date", "car", "user_m", "user_t", "user_n"]

    dicio = []
    for reserv in agenda:
        dicio.append( dict( zip(header, reserv)) )

    response = make_response( jsonify(dicio), 200 )
    response.headers["Content-Type"] = "application/json"
    return response

