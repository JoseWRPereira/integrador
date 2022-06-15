from flask import Blueprint, redirect, render_template, url_for
from flask import flash, session
from app.users.form import FormUserCreate, FormLogin
from app.db.dbcon import DBConn


users_bp = Blueprint('users_bp',__name__,
                    template_folder='templates')


@users_bp.route("/user_login", methods=['GET','POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        if form.errors:
            flash('{}'.format(form.errors),'alert')
        else:
            db = DBConn()
            u = db.sql_fetch("SELECT id,name,email,password,nif,admin FROM users WHERE email='{}';".format(form.email.data) )
            if u:
                if u[0][3] != str(form.password.data):
                    flash('Senha incorreta!','alert')
                else:
                    session['id']       = u[0][0]
                    session['username'] = u[0][1]
                    session['email']    = u[0][2]
                    session['nif']      = u[0][4]
                    session['admin']    = u[0][5]
                    return redirect(url_for('index'))
            else:
                flash('Usuário não encontrado/cadastrado!','alert')
    return render_template('user_login.html', form_login=form)



@users_bp.route("/user_logout")
def logout():
    session.pop('username', None)
    session.pop('email',    None)
    session.pop('id',       None)
    session.pop('nif',      None)
    session.pop('admin',    None)
    return redirect(url_for('users_bp.login'))


@users_bp.route("/create_user", methods=['GET','POST'])
def create_user():
    form = FormUserCreate()
    if form.validate_on_submit():
        if form.errors:
            flash('{}'.format(form.errors),'alert')
        elif form.password.data != form.password_confirm.data:
            flash('Senhas diferentes!','alert')
        else:
            db = DBConn()
            user_id  = db.sql_fetch("SELECT id FROM users WHERE email='{}';".format(str(form.email.data) ))
            user_nif = db.sql_fetch("SELECT id FROM users WHERE nif='{}';".format(str(form.nif.data) ))
            if user_id or user_nif:
                flash('Usuário já cadastrado!','alert')
            else:
                db.sql_cmd("INSERT INTO users ( name, email, password, nif, admin) VALUES ('{}','{}','{}','{}',False);".format( form.name.data, form.email.data, form.password.data, form.nif.data) )
                return redirect(url_for('users_bp.login'))
    return render_template('user_create.html', form_user=form )


@users_bp.route("/delete_user/<int:id>")
def users_delete(id):
    form = FormUserCreate()
    if 'username' in session:
        if session['admin'] == True and session['id'] != id:
            db = DBConn()
            db.sql_cmd("DELETE FROM users WHERE id='{}';".format(id) )
        else:
            flash('Operação não permitida!','alert')
    else:
        flash('Usuário não logado!','alert')
    return redirect(url_for('users_bp.users_manager'))



@users_bp.route("/edit_user/<int:id>", methods=['GET', 'POST'])
def users_edit(id):
    form = FormUserCreate()
    if 'username' in session:
        if form.validate_on_submit():
            if form.errors:
                flash('{}'.format(form.errors),'alert')
            else:
                db = DBConn()
                db.sql_cmd("UPDATE users SET name='{}', email='{}', password='{}', nif='{}'  WHERE id='{}';".format(form.name.data, form.email.data, form.password.data, form.nif.data, id ) )
            return redirect(url_for('users_bp.users_manager'))
        else:
            db = DBConn()
            u = db.sql_fetch("SELECT name,email,nif,admin FROM users WHERE id='{}';".format(id) )
            if u:
                form.name.data   = u[0][0]
                form.email.data  = u[0][1]
                form.nif.data    = u[0][2]
            else:
                flash('Usuário não encontrado!','alert')
            return render_template('user_create.html', form_user=form)
    else:
        return redirect(url_for('index'))



@users_bp.route("/users_manager", methods=['GET','POST'])
def users_manager():
    form = FormUserCreate()
    if 'username' in session:
        if session['admin'] == True:
            db = DBConn()
            users = db.sql_fetch("SELECT id,name,email,nif,admin FROM users;")
        else:
            db = DBConn()
            users = db.sql_fetch("SELECT id,name,email,nif,admin FROM users WHERE id='{}';".format(session['id']))
        return render_template('users_manager.html', users=users )
    else:
        return redirect(url_for('index'))
