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
    nif = StringField("nif", validators=[DataRequired()])

class EditUserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    nif = StringField("nif", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])


    def selectUser(self, id ):
        usr = db.sql_fetch("SELECT id,nome,email,password,nif,admin FROM users WHERE id='{}';".format( id ))
        self.name.data = str(usr[0][1])
        self.email.data = usr[0][2]
        self.password.data = usr[0][3]
        self.nif.data = usr[0][4]
    
    def saveUser(self, id):
        db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}', nif='{}' WHERE id={};".format(self.name.data, self.email.data, self.password.data, self.nif.data, id) )


class User():

    def login_validate(self, email, password ):
        user = db.sql_fetch("SELECT id,name,email,password,nif,admin FROM users WHERE email='{}';".format(str(email) ))
        if user:
            if user[0][3] != str(password):
                flash('Senha incorreta!','alert')
                return False
            else:
                session['id'] = user[0][0]
                session['username'] = user[0][1]
                session['email'] = user[0][2]
                session['nif'] = user[0][4]
                session['admin'] = user[0][5]
                return True
        else:
            flash('Usuário não cadastrado!','alert')
            return False


    def logout(self):
        session.pop('username', None)
        session.pop('email', None)
        session.pop('id', None)
        session.pop('nif', None)
        session.pop('admin', None)


    def newuser_validate(self, name, email, password, nif):
        user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(email) ))
        user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(nif) ))
        if user_id or user_nif:
            flash('Usuário já cadastrado!','alert')
            return False
        else:
            db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( name, email, password, nif) )
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






class Agenda():
    def lst(self):
        registros = db.sql_fetch("SELECT id,name FROM cars;")

        mask = ['','m','t','n']
        lst = []
        for campo in registros:
            reg = db.sql_fetch("SELECT car,user_m,user_t,user_n FROM reservations WHERE res_date='{}' AND car='{}' ORDER BY id ASC;".format(session['reservation_date'], campo[0]) )
            sub = []
            if reg:
                for i in range(0,4):
                    if reg[0][i] != None:
                        sub.append(reg[0][i])
                    else:
                        sub.append(mask[i])
            else:
                sub.append(campo[0])
                sub.append(mask[1])
                sub.append(mask[2])
                sub.append(mask[3])
            lst.append(sub)
        return lst

