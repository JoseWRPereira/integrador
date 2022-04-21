from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = EmailField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
