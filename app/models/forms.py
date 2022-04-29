from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.models.db import DBConn



####################################### 
####################################### Auth
####################################### 

class FormLogin(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

    def login(self):
        db = DBConn()
        u = db.sql_fetch("SELECT id,name,email,password,nif,admin FROM users WHERE email='{}';".format(self.email.data) )
        if u:
            if u[0][3] != str(self.password.data):
                flash('Senha incorreta!','alert')
                return False
            else:
                session['id']       = u[0][0]
                session['username'] = u[0][1]
                session['email']    = u[0][2]
                session['nif']      = u[0][4]
                session['admin']    = u[0][5]
                return True
        else:
            flash('Usuário não encontrado/cadastrado!','alert')
            return False

    def logout(self):
        session.pop('username', None)
        session.pop('email',    None)
        session.pop('id',       None)
        session.pop('nif',      None)
        session.pop('admin',    None)


####################################### 
####################################### User
####################################### 


class FormUserCreate(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])
    nif = StringField("nif", validators=[DataRequired()])

    def create(self):
        db = DBConn()
        user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(self.email.data) ))
        user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(self.nif.data) ))
        if user_id or user_nif:
            flash('Usuário já cadastrado!','alert')
            return False
        else:
            db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( self.name.data, self.email.data, self.password.data, self.nif.data) )
            return True

    def read(self,id):
        db = DBConn()
        u = db.sql_fetch("SELECT name,email,nif,admin FROM users WHERE id='{}';".format(id) )
        if u:
            self.name.data   = u[0][0]
            self.email.data  = u[0][1]
            self.nif.data    = u[0][2]
            return True
        else:
            flash('Usuário não encontrado!','alert')
            return False

    def get_all(self):
        db = DBConn()
        u = db.sql_fetch("SELECT id,name,email,nif,admin FROM users;")
        return u

    def get_one(self, id):
        db = DBConn()
        u = db.sql_fetch("SELECT id,name,email,nif,admin FROM users WHERE id='{}';".format(id))
        return u

    def update(self,id):
        db = DBConn()
        db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}', nif='{}'  WHERE id='{}';".format(self.name.data, self.email.data, self.password.data, self.nif.data, id ) )
        return True

    def delete(self,id):
        db = DBConn()
        db.sql_cmd("DELETE FROM users WHERE id='{}';".format(id) )
        return True


####################################### 
####################################### Car
####################################### 

class FormCar(FlaskForm):
    name = StringField("name", validators=[DataRequired()])

    def select(self, id):
        db = DBConn()
        lst = db.sql_fetch("SELECT id,name FROM cars WHERE id='{}';".format( id ))
        self.name.data = str(lst[0][1])
        return lst

    def update(self, id):
        db = DBConn()
        db.sql_cmd("UPDATE cars SET name='{}' WHERE id='{}';".format(self.name.data, id) )

    def is_valid(self):
        db = DBConn()
        existe = db.sql_fetch("SELECT id FROM cars WHERE name='{}';".format(self.name.data) )
        if existe:
            return False
        else:
            return True

    def insert(self):
        db = DBConn()
        db.sql_cmd("INSERT INTO cars (name) VALUES ('{}');".format( self.name.data) )

    def delete(self, id):
        db = DBConn()
        db.sql_cmd("DELETE FROM cars WHERE id='{}';".format(id) )

    def list_all(self):
        db = DBConn()
        lst = db.sql_fetch("SELECT id,name FROM cars;")
        return lst




####################################### 
####################################### Agenda
####################################### 

class Agenda():
    def lst(self):
        db = DBConn()
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
