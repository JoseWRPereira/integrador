from crypt import methods
from flask import Flask, redirect, request
from flask import render_template
from flask import url_for
from flask import flash

app = Flask(__name__)
app.secret_key = 'dont tell anyone'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['senha']
        if user == 'admin@email.com' and password == 'admin':
            # return redirect( url_for('index'))
            return "OK"
        else:
            flash('Login incorreto! Tente outra vez...','alert')
            return redirect( url_for('login'))
    else:
        return render_template('login.html')

@app.route("/newuser", methods=['GET','POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['nome']
        email = request.form['email']
        password = request.form['passwd']
        confirm = request.form['confirm']
        if password == confirm:
            # return redirect( url_for('index'))
            return "OK"
        else:
            flash('Senhas diferentes!','alert')
            return redirect( url_for('newuser'))
    else:
        return render_template('newuser.html')


if __name__=='__main__':
    app.run()
