from flask import Flask
# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

# lm = LoginManager()
# lm.init_app(app)

from app.controllers import default
