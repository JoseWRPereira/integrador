from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class FormEquipment(FlaskForm):
    name = StringField("name", validators=[DataRequired()])

