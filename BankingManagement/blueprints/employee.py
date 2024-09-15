import random
from flask import Blueprint, render_template, request, jsonify
from bson import ObjectId

from models import database

from helpers import login_required, paginator
from datetime import datetime, date

db = database.Database().get_db()
employee = db['employees']
salary = db['salary']

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

def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@employee_blueprint.route('/employee/home', methods = ['GET'])
def employee_home():
    if request.method == 'GET':
        # max_STT_doc = db.employee.find().sort('STT', -1).limit(1).next()
        # max_STT = max_STT_doc["STT"]
        # new_docs = []
        # for doc in data:
        #     new_doc = {k:v for k,v in doc.items() if k != '_id'} #remove the _id
        #     max_STT += 1
        #     new_doc['STT'] = max_STT
        #     new_doc["CreatedDate"] = datetime(2024, 7, 1).isoformat()
        #     new_docs.append(new_doc)

        # db.employee.insert_many(new_docs)
        today = date.today()
        current_month = today.strftime("%B")
        current_year = today.year

         # Construct MongoDB query to filter documents based on month and year
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)
        start_date_iso = start_date.isoformat()
        end_date_iso = end_date.isoformat()

        query = {'CreatedDate': {'$gte': start_date_iso, '$lt': end_date_iso}}
        data = list(db.employee.find(query))
        data = convert_objectid(data)
        return render_template('employee/home.html', current_month = current_month, current_year = current_year, months=months, years=years, fake_data=data)

@employee_blueprint.route('/get-data', methods=['POST'])
def get_data():
    # Check if the request contains JSON data
    if request.is_json:
        try:
            # get json from body of the request
            data = request.get_json()
            month_str = data['month']
            year = int(data['year'])
            
            if month_str not in month_map.keys():
                return jsonify({'error': 'Invalid month name'}), 400

            month = month_map[month_str]
            # Construct MongoDB query to filter documents based on month and year
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            start_date_iso = start_date.isoformat()
            end_date_iso = end_date.isoformat()

            query = {'CreatedDate': {'$gte': start_date_iso, '$lt': end_date_iso}}

            # Execute the query and convert the cursor to a list
            data_cursor = db.employee.find(query)
            data_list = list(data_cursor)  # Convert cursor to list
            
            if not data_list:
                print("No documents found for the given query.")
            # Convert MongoDB ObjectId to string
            for doc in data_list:
                doc['_id'] = str(doc['_id'])
                doc['Sex'] = 'Male' #example, fix this later 
            
            return jsonify(data_list), 200
        except KeyError:
            return jsonify({'error': 'Invalid input data. "month" and "year" are required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Request does not contain JSON'}), 400


@employee_blueprint.route('/employee/working-time', methods = ['GET'])
def employee_working_time():
    if request.method == 'GET':
        return render_template('employee/working_time.html')
    
@employee_blueprint.route('/employee/salary', methods = ['GET'])
def employee_salary():
    if request.method == 'GET':
        return  render_template('employee/salary.html') 
    
@employee_blueprint.route('/employee', methods = ['GET'])
@login_required
def employee():
    page = request.args.get('page', 1, int)
    dataType = request.args.get('dataType')
    year = request.args.get('year')
    if year is not None:
        try:
            year = int(year)
        except ValueError:
            # Handle the error if the conversion fails, e.g., log the error or set a default value
            year = datetime.now().year  #  default current year
    else:
        year = datetime.now().year  #  default current year

    query = {'CreatedDate': {
        '$gte': datetime(year, 1, 1).isoformat(),
        '$lt': datetime(year + 1, 1, 1).isoformat()
    }}
    if dataType == 'salary':
        items = list(salary.find(query, {'_id': 0}))
            
    pagination = paginator(page, items)
    return jsonify({'items': pagination['render_items'], 'total_pages': pagination['total_pages']})
    

