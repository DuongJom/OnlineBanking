from flask import Blueprint, request, redirect, url_for, flash
from datetime import datetime
from models import database, workingDayInfo
from message import messages
from SysEnum import WorkingType, EmployeeStatusType

db = database.Database().get_db()
employees = db['employees']

employee_blueprint = Blueprint('employee', __name__)

@employee_blueprint.route('/employee/check-in/<id>', methods=['PUT'])
def check_in(id):
    if request.method == 'PUT':

        filter = {'_id': id}
        employee = employees.find_one(filter)

        if employee is not None:
            checked_in_time = datetime.strptime(employee['Check_in_time'], '%Y-%m-%d %H:%M:%S')
            if checked_in_time.day == datetime.now().day and \
                checked_in_time.month == datetime.now().month and \
                checked_in_time.year == datetime.now().year:
                flash(messages['employee_already_checked_in'])
                return redirect(url_for('/home'))
            
            updated_data = {
                'Check_in_time': datetime.now(),
                'Status': EmployeeStatusType.WORKING.value,
                'Working_days': employee['Working_days'].append(workingDayInfo.WorkingDays(day=datetime.now().day, 
                                                                                           month=datetime.now().month, 
                                                                                           year=datetime.now().year),
                                                                                           workingStatus=WorkingType.WORKING.value)
            }
            employees.update_one(filter, {'$set': updated_data})
        else:
            flash(messages["employee_not_exist"].format(id))
            return redirect(url_for("home"))
        
        

        