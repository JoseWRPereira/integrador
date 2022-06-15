from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.db.dbcon import DBConn


class FormLogin(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class FormUserCreate(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])
    nif = StringField("nif", validators=[DataRequired()])
