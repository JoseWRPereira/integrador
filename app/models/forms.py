from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.models.db import DBConn


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class NewUserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])


class User():
    def __init__(self):
        self.id = 0
        self.name = "Convidado"
        self.email = ""
        self.password = ""


    def logged_in(self):
        if self.id != 0:
            return True
        else:
            return False


    def login_validate(self, email, password ):
        db = DBConn()
        user = db.sql_fetch("SELECT * FROM users WHERE email='{}';".format(str(email) ))
        if user:
            if user[0][3] != str(password):
                flash('Senha incorreta!','alert')
                return False
            else:
                self.id = user[0][0]
                self.name = user[0][1]
                self.email = user[0][2]
                self.password = user[0][3]
                session['username'] = str(self.name)
                session['email'] = str(self.email)
                session['id'] = self.id
                print( session['username'] )
                return True
        else:
            flash('Usuário não cadastrado!','alert')
            return False


    def newuser_validate(self, name, email, password):
        db = DBConn()
        user_id = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(email) ))
        if user_id:
            flash('Usuário já cadastrado!','alert')
            return False
        else:
            db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( name, email, password) )
            return True

