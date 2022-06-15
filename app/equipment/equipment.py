from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import session, flash
from app.db.dbcon import DBConn
from app.equipment.forms import FormEquipment

equipment_bp = Blueprint('equipment_bp', __name__, template_folder='templates')


# class Equipment():
#     def select(self, id):
#         db = DBConn()
#         lst = db.sql_fetch("SELECT id,name FROM cars WHERE id='{}';".format( id ))
#         self.name.data = str(lst[0][1])
#         return lst

#     def update(self, id):
#         db = DBConn()
#         db.sql_cmd("UPDATE cars SET name='{}' WHERE id='{}';".format(self.name.data, id) )

#     def is_valid(self):
#         db = DBConn()
#         existe = db.sql_fetch("SELECT id FROM cars WHERE name='{}';".format(self.name.data) )
#         if existe:
#             return False
#         else:
#             return True

#     def insert(self):
#         db = DBConn()
#         db.sql_cmd("INSERT INTO cars (name) VALUES ('{}');".format( self.name.data) )

#     def delete(self, id):
#         db = DBConn()
#         db.sql_cmd("DELETE FROM cars WHERE id='{}';".format(id) )

#     def list_all(self):
#         db = DBConn()
#         lst = db.sql_fetch("SELECT id,name FROM cars;")
#         return lst


@equipment_bp.route('/cars_manager', methods=['GET', 'POST'])
def equipment_manager():
    if 'username' in session:
        form = FormEquipment()
        if 'equipment_edit_id' in session:
            # equipment.select( session['equipment_edit_id'] )
            db = DBConn()
            lst = db.sql_fetch("SELECT id,name FROM cars WHERE id='{}';".format( session['equipment_edit_id'] ))
            form.name.data = str( lst[0][1] )
        if form.validate_on_submit():
            if form.errors:
                flash('{}'.format(form.errors),'alert')
            else:
                if 'equipment_edit_id' in session:
                    # equipment.update(session['equipment_edit_id'])
                    db = DBConn()
                    db.sql_cmd("UPDATE cars SET name='{}' WHERE id='{}';".format(form.name.data, session['equipment_edit_id']) )

                    session.pop('equipment_edit_id', None)
                    return redirect( url_for('equipment_bp.equipment_manager'))
                else:
                    # if equipment.is_valid():
                    #     equipment.insert()
                    db = DBConn()
                    existe = db.sql_fetch("SELECT id FROM cars WHERE name='{}';".format(form.name.data) )
                    if not existe:
                        # return True

                # def insert(self):
                        db = DBConn()
                        db.sql_cmd("INSERT INTO cars (name) VALUES ('{}');".format( form.name.data) )

                    else:
                        flash('Carrinho já existe!','alert')
                    return redirect( url_for('equipment_bp.equipment_manager'))
        # car_list=equipment.list_all()
#!@#
        db = DBConn()
        car_list = db.sql_fetch("SELECT id,name FROM cars;")

        return render_template('cars_manager.html', form_car=form, cars=car_list )
    else:
        return redirect( url_for('index'))





@equipment_bp.route("/delete_car/<int:id>")
def equipment_delete(id):
    if 'username' in session:
        if session['admin'] == True:
            # equipment = Equipment()
            # equipment.delete(id)
            db = DBConn()
            db.sql_cmd("DELETE FROM cars WHERE id='{}';".format(id) )
    return redirect(url_for('equipment_bp.equipment_manager'))



@equipment_bp.route("/edit_car/<int:id>")
def equipment_edit(id):
    if 'username' in session:
        if session['admin'] == True:
            session['equipment_edit_id'] = id
    return redirect(url_for('equipment_bp.equipment_manager'))
