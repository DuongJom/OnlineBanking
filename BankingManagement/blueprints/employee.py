import json
from flask import Blueprint, render_template, request, jsonify
from models import database
from datetime import datetime, date

db = database.Database().get_db()
employee = db['employees']

employee_blueprint = Blueprint('employee', __name__)

years = list(range(2000, 2101))
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
# Mapping of month names to numbers
month_map = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

@employee_blueprint.route('/employee/home', methods = ['GET'])
def employee_home():
    if request.method == 'GET':
        fake_data = [
        {"STT": 1, "Employee ID": "EMP001", "Employee Name": "John Doe", "Role": "Manager",
         "Check-in time": "08:00 AM", "Check-out time": "05:00 PM", "Status": "Present"},
        {"STT": 2, "Employee ID": "EMP002", "Employee Name": "Jane Smith", "Role": "Developer",
         "Check-in time": "09:00 AM", "Check-out time": "06:00 PM", "Status": "Present"},
        ]
        today = date.today()
        current_month = today.strftime("%B")
        current_year = today.year
        return render_template('employee/home.html', current_month = current_month, current_year = current_year, months=months, years=years, fake_data=fake_data)

@employee_blueprint.route('/get-data', methods=['POST'])
def get_data():
    # Check if the request contains JSON data
    if request.is_json:
        try:
            # get json from body of the request
            data = request.get_json()
            month_str = data['month']
            year = int(data['year'])
            
            if month_str not in month_map:
                return jsonify({'error': 'Invalid month name'}), 400

            month = month_map[month_str]
            # Construct MongoDB query to filter documents based on month and year
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            start_date_iso = start_date.isoformat()
            end_date_iso = end_date.isoformat()

            query = {'CreatedDate': {'$gte': start_date_iso, '$lt': end_date_iso}}

            # Execute the query and convert the cursor to a list
            data_cursor = db.users.find(query)
            data_list = list(data_cursor)  # Convert cursor to list
            if not data_list:
                print("No documents found for the given query.")
            # Convert MongoDB ObjectId to string
            for doc in data_list:
                doc['_id'] = str(doc['_id'])
                doc['Sex'] = 'Male' if doc['Sex'] == '1' else 'Female'

            return jsonify(data_list), 200
        except KeyError:
            return jsonify({'error': 'Invalid input data. "month" and "year" are required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Request does not contain JSON'}), 400

    


    