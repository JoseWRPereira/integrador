from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
#from app.models.db import DBConn
# from app.db import DBConn


class FormEquipment(FlaskForm):
    name = StringField("name", validators=[DataRequired()])

