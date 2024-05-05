from flask import Blueprint, render_template, request

employee_blueprint = Blueprint('employee', __name__)

@employee_blueprint.route('/employee/home', methods = ['GET'])
def employee_home():
    if request.method == 'GET':
        return render_template('employee/home.html')