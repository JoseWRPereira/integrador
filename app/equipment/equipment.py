from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import session, flash
from app.equipment import forms

equipment_bp = Blueprint('equipment_bp', __name__, template_folder='templates')


@equipment_bp.route('/equipment_manager', methods=['GET', 'POST'])
def equipment_manager():
    if 'username' in session:
        equipment = forms.FormEquipment()
        if 'equipment_edit_id' in session:
            equipment.select( session['equipment_edit_id'] )

        if equipment.validate_on_submit():
            if equipment.errors:
                flash('{}'.format(equipment.errors),'alert')
            else:
                if 'car_edit_id' in session:
                    equipment.update(session['equipment_edit_id'])
                    session.pop('equipment_edit_id', None)
                    return redirect( url_for('equipment_manager'))
                else:
                    if equipment.is_valid():
                        equipment.insert()
                    else:
                        flash('Carrinho já existe!','alert')
                    return redirect( url_for('equipment_manager'))
        car_list=equipment.list_all()
        return render_template('equipment_manager.html', form_car=equipment, cars=car_list )
    else:
        return redirect( url_for('index'))





@equipment_bp.route("/delete_equipment/<int:id>")
def equipment_delete(id):
    if 'username' in session:
        if session['admin'] == True:
            equipment = forms.FormEquipment()
            equipment.delete(id)
    return redirect(url_for('equipment_manager'))



@equipment_bp.route("/edit_equipment/<int:id>")
def equipment_edit(id):
    if 'username' in session:
        if session['admin'] == True:
            session['equipment_edit_id'] = id
    return redirect(url_for('equipment_manager'))
