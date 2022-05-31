from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired
from app.models.db import DBConn



class FormEquipment(FlaskForm):
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
