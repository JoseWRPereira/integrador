from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.db.dbcon import DBConn


####################################### 
####################################### Auth
####################################### 

class FormLogin(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


# class Auth():
    # def login(self):
    #     db = DBConn()
    #     u = db.sql_fetch("SELECT id,name,email,password,nif,admin FROM users WHERE email='{}';".format(self.email.data) )
    #     if u:
    #         if u[0][3] != str(self.password.data):
    #             flash('Senha incorreta!','alert')
    #             return False
    #         else:
    #             session['id']       = u[0][0]
    #             session['username'] = u[0][1]
    #             session['email']    = u[0][2]
    #             session['nif']      = u[0][4]
    #             session['admin']    = u[0][5]
    #             return True
    #     else:
    #         flash('Usuário não encontrado/cadastrado!','alert')
    #         return False

    # def logout(self):
    #     session.pop('username', None)
    #     session.pop('email',    None)
    #     session.pop('id',       None)
    #     session.pop('nif',      None)
    #     session.pop('admin',    None)


####################################### 
####################################### User
####################################### 


class FormUserCreate(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired()])
    nif = StringField("nif", validators=[DataRequired()])


# class User():
#     def create(self):
#         db = DBConn()
#         user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(self.email.data) ))
#         user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(self.nif.data) ))
#         if user_id or user_nif:
#             flash('Usuário já cadastrado!','alert')
#             return False
#         else:
#             db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( self.name.data, self.email.data, self.password.data, self.nif.data) )
#             return True

#     def read(self,id):
#         db = DBConn()
#         u = db.sql_fetch("SELECT name,email,nif,admin FROM users WHERE id='{}';".format(id) )
#         if u:
#             self.name.data   = u[0][0]
#             self.email.data  = u[0][1]
#             self.nif.data    = u[0][2]
#             return True
#         else:
#             flash('Usuário não encontrado!','alert')
#             return False

#     def get_all(self):
#         db = DBConn()
#         u = db.sql_fetch("SELECT id,name,email,nif,admin FROM users;")
#         return u

#     def get_one(self, id):
#         db = DBConn()
#         u = db.sql_fetch("SELECT id,name,email,nif,admin FROM users WHERE id='{}';".format(id))
#         return u

#     def update(self,id):
#         db = DBConn()
#         db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}', nif='{}'  WHERE id='{}';".format(self.name.data, self.email.data, self.password.data, self.nif.data, id ) )
#         return True

#     def delete(self,id):
#         db = DBConn()
#         db.sql_cmd("DELETE FROM users WHERE id='{}';".format(id) )
#         return True
