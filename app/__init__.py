from flask import Flask
from app.api.v1 import api_bp

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api_bp)

from app.controllers import default

