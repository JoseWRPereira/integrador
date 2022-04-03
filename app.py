from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Integrador"


if __name__=='__main__':
    app.run()