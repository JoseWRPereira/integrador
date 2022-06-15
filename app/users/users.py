from flask import Blueprint, redirect, render_template, url_for
from flask import flash, session
from app.users.form import FormUserCreate, FormLogin
from app.db.dbcon import DBConn
# from .forms import AuthForm, UserNew
# from app.db.dbcon import DBConn
# from app.users.form import FormLogin, Auth, FormUserCreate, User



users_bp = Blueprint('users_bp',__name__,
                    template_folder='templates')



# class User():
#     def create(self, name, email, password, nif):
#         db = DBConn()
#         user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(email) ))
#         user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(nif) ))
#         if user_id or user_nif:
#             flash('Usuário já cadastrado!','alert')
#             return False
#         else:
#             db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( name, email, password, nif) )
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






@users_bp.route("/user_login", methods=['GET','POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        if form.errors:
            flash('{}'.format(form.errors),'alert')
        else:
            # if form.login():

        # def login(self):
            db = DBConn()
            u = db.sql_fetch("SELECT id,name,email,password,nif,admin FROM users WHERE email='{}';".format(form.email.data) )
            if u:
                if u[0][3] != str(form.password.data):
                    flash('Senha incorreta!','alert')
                    # return False
                else:
                    session['id']       = u[0][0]
                    session['username'] = u[0][1]
                    session['email']    = u[0][2]
                    session['nif']      = u[0][4]
                    session['admin']    = u[0][5]
                    return redirect(url_for('index'))
                    # return True
            else:
                flash('Usuário não encontrado/cadastrado!','alert')
                # return False


                # return redirect(url_for('index'))
    return render_template('user_login.html', form_login=form)



@users_bp.route("/user_logout")
def logout():
    # return auth.logout()
    # user = FormLogin()
    # user.logout()
    # def logout(self):
    session.pop('username', None)
    session.pop('email',    None)
    session.pop('id',       None)
    session.pop('nif',      None)
    session.pop('admin',    None)
    return redirect(url_for('users_bp.login'))








####################################### 
####################################### User
####################################### 

# class User():
#     def create(self):
#         user = FormUserCreate()
#         if user.validate_on_submit():
#             if user.errors:
#                 flash('{}'.format(user.errors),'alert')
#             elif user.password.data != user.password_confirm.data:
#                 flash('Senhas diferentes!','alert')
#             else:
#                 if user.create():
#                     return redirect(url_for('login'))
#         return render_template('user_create.html', form_user=user )











@users_bp.route("/create_user", methods=['GET','POST'])
def create_user():
    # return user.create()
    # def create(self):
    form = FormUserCreate()
    if form.validate_on_submit():
        if form.errors:
            flash('{}'.format(form.errors),'alert')
        elif form.password.data != form.password_confirm.data:
            flash('Senhas diferentes!','alert')
        else:
        #     user = User()
        # def create(self, name, email, password, nif):
            db = DBConn()
            user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(form.email.data) ))
            user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(form.nif.data) ))
            if user_id or user_nif:
                flash('Usuário já cadastrado!','alert')
                # return False
            else:
                db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( form.name.data, form.email.data, form.password.data, form.nif.data) )
            #     return True

            # if user.create():
                return redirect(url_for('users_bp.login'))
    return render_template('user_create.html', form_user=form )


@users_bp.route("/delete_user/<int:id>")
def users_delete(id):
    # return user.manager_delete(id)
    # def manager_delete(self,id):
    form = FormUserCreate()
    if 'username' in session:
        if session['admin'] == True and session['id'] != id:
            # user.delete(id)
            db = DBConn()
            db.sql_cmd("DELETE FROM users WHERE id='{}';".format(id) )
        else:
            flash('Operação não permitida!','alert')
    else:
        flash('Usuário não logado!','alert')
    return redirect(url_for('users_bp.users_manager'))



@users_bp.route("/edit_user/<int:id>", methods=['GET', 'POST'])
def users_edit(id):
    # return user.edit(id)
    # def edit(self,id):
    form = FormUserCreate()
    if 'username' in session:
        if form.validate_on_submit():
            if form.errors:
                flash('{}'.format(form.errors),'alert')
            else:
                # user.update(id)
                db = DBConn()
                db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}', nif='{}'  WHERE id='{}';".format(form.name.data, form.email.data, form.password.data, form.nif.data, id ) )
            return redirect(url_for('users_bp.users_manager'))
        else:
            # user.read(id)
            db = DBConn()
            u = db.sql_fetch("SELECT name,email,nif,admin FROM users WHERE id='{}';".format(id) )
            if u:
                form.name.data   = u[0][0]
                form.email.data  = u[0][1]
                form.nif.data    = u[0][2]
                # return True
            else:
                flash('Usuário não encontrado!','alert')
                # return False
            return render_template('user_create.html', form_user=form)
    else:
        return redirect(url_for('index'))



@users_bp.route("/users_manager", methods=['GET','POST'])
def users_manager():
    # return user.manager()
    # def manager(self):
    form = FormUserCreate()
    if 'username' in session:
        if session['admin'] == True:
            # users = user.get_all()
        # def get_all(self):
            db = DBConn()
            users = db.sql_fetch("SELECT id,name,email,nif,admin FROM users;")
        else:
            # users = user.get_one(session['id'])
        # def get_one(self, id):
            db = DBConn()
            users = db.sql_fetch("SELECT id,name,email,nif,admin FROM users WHERE id='{}';".format(session['id']))
            # return u
        return render_template('users_manager.html', users=users )
    else:
        return redirect(url_for('index'))
