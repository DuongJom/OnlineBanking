from flask import Blueprint, render_template, request, jsonify
from models import database
from datetime import datetime

db = database.Database().get_db()
employee = db['employees']

employee_blueprint = Blueprint('employee', __name__)


@employee_blueprint.route('/employee/home', methods = ['GET'])
def employee_home():
    if request.method == 'GET':
        return render_template('employee/home.html')

@employee_blueprint.route('/get_data', methods=['POST'])
def get_data():
    month = request.form['month']
    year = request.form['year']
    # Construct MongoDB query to filter documents based on month and year
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    query = {'CreatedDate': {'$gte': start_date, '$lt': end_date}}
    # Execute the query and return the results
    data = list(employee.find(query))
    return jsonify(data)
