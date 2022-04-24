from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.models.db import DBConn


db = DBConn()



class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class NewUserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])


class EditUserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])


    def selectUser(self, id ):
        # db = DBConn()
        usr = db.sql_fetch("SELECT * FROM users WHERE id='{}';".format( id ))
        print( usr[0][0] )
        print( usr[0][1] )
        print( usr[0][2] )
        print( usr[0][3] )
        self.name.data = str(usr[0][1])
        self.email.data = usr[0][2]
        self.password.data = usr[0][3]
    
    def saveUser(self, id):
        # db = DBConn()
        print( id )
        print( self.name.data )
        print( self.email.data )
        print( self.password.data)
        db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}' WHERE id={};".format(self.name.data, self.email.data, self.password.data, id) )


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
        # db = DBConn()
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
        # db = DBConn()
        user_id = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(email) ))
        if user_id:
            flash('Usuário já cadastrado!','alert')
            return False
        else:
            db.sql_cmd("INSERT INTO users ( name, email, password) VALUES ('{}','{}','{}');".format( name, email, password) )
            return True










class CarForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])


    def select(self, id):
        lst = db.sql_fetch("SELECT id,name FROM cars WHERE id='{}';".format( id ))
        self.name.data = str(lst[0][1])
        return lst


    def update(self, id):
        db.sql_cmd("UPDATE cars SET name='{}' WHERE id='{}';".format(self.name.data, id) )


    def is_valid(self):
        existe = db.sql_fetch("SELECT id FROM cars WHERE name='{}';".format(self.name.data) )
        if existe:
            return False
        else:
            return True


    def insert(self):
        db.sql_cmd("INSERT INTO cars (name) VALUES ('{}');".format( self.name.data) )


    def delete(self, id):
        db.sql_cmd("DELETE FROM cars WHERE id='{}';".format(id) )


    def list_all(self):
        lst = db.sql_fetch("SELECT id,name FROM cars;")
        return lst