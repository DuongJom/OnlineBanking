from flask import Blueprint, request, redirect, url_for, flash
from datetime import datetime
from models import database, employee
from message import messages
from SysEnum import WorkingStatusEnum

db = database.Database().get_db()
employees = db['employees']

employee_blueprint = Blueprint('employee', __name__)

@employee_blueprint.route('/employee/check-in/<id>', methods=['PUT'])
def check_in(id):
    if request.method == 'PUT':
        filter = {'_id': id}
        updated_data = {
            'Check_in_time': datetime.now(),
            'Working_status': WorkingStatusEnum.WORKING.value,
        }
        employee = employees.find_one(filter)

        if employee is not None:
            checked_in_time = datetime.strptime(employee['Check_in_time'], '%Y-%m-%d %H:%M:%S')
            if checked_in_time.day == datetime.now().day and \
                checked_in_time.month == datetime.now().month and \
                checked_in_time.year == datetime.now().year:
                flash(messages['employee_already_checked_in'])
                return redirect(url_for('/home'))
            employees.update_one(filter, {'$set': updated_data})
        else:
            flash(messages["employee_not_exist"].format(id))
            return redirect(url_for("home"))
        
@employee_blueprint.route('/employee/check-out/<id>', methods=['PUT'])
def check_out(id):
    if request.method == 'PUT':
        filter = {'_id': id}
        updated_data = {
            'Check_out_time': datetime.now()
        }
        employee = employees.find_one(filter)

        if employee is not None:
            employees.update_one(filter, {'$set': updated_data})
        else:
            flash(messages["invalid_information"])
            return redirect(url_for("home"))