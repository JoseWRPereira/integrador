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
    users = db.sql_fetch("SELECT * from users;")
    header = ["id", "name", "email", "password", "nif", "admin"]

    dicio = []
    for user in users:
        dicio.append( dict( zip(header, user)) )

    response = make_response( jsonify(dicio), 200 )
    response.headers["Content-Type"] = "application/json"
    return response
