from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class NewUserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])

