from flask import Flask, render_template
from app.db.database import database_bp
from app.users.users import users_bp
from app.equipment.equipment import equipment_bp
from app.scheduling.agenda import agenda_bp
from app.api.v1 import api_bp

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(database_bp)
app.register_blueprint(users_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(agenda_bp)
app.register_blueprint(api_bp)

@app.route("/")
def index():
    return render_template('index.html')
