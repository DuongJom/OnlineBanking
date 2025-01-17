from flask import Blueprint, render_template, request, jsonify, session
from bson import ObjectId
from datetime import datetime, date

from models import database
from helpers import login_required, paginator
from enums.month_type import MonthType


db = database.Database().get_db()
accounts = db['accounts']
employees = db['employees']
salary = db['salary']

employee_blueprint = Blueprint('employee', __name__)

years = list( range(2000, date.today().year + 1) )
months = []
for month in MonthType:
    months.append(month.name.capitalize())

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
        today = date.today()
        current_month = today.strftime("%B")
        current_year = today.year

        # Construct MongoDB query to filter documents based on month and year
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)

        start_date_iso = start_date.isoformat()
        end_date_iso = end_date.isoformat()

        query = {'CreatedDate': {'$gte': start_date_iso, '$lte': end_date_iso}}
        data = list(db['employee'].find(query))
        return render_template('employee/home.html', current_month = current_month, current_year = current_year, months=months, years=years, fake_data=data)


#return home data
@employee_blueprint.route('/get-home-data', methods=['POST'])
def get_home_data():
    # Check if the request contains JSON data
    if request.is_json:
        try:
            # get json from body of the request
            data = request.get_json()
            month_str = data['month'].upper()
            for item in (MonthType):
                if month_str == item.name:
                    month = item.value

            year = int(data['year'])
            
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
        today = datetime.now()
        formated_month_year = today.strftime("%m/%y")
        formated_date_month = today.strftime("%d/%m")
        return render_template('employee/working_time.html', month_year = formated_month_year, date_month = formated_date_month)

#get working time data
@employee_blueprint.route('/get-working-time-data', methods=['POST'])
def get_working_time_data():
    # Check if the request contains JSON data
    if request.is_json:
        try:
            # get json from body of the request
            data = request.get_json()
            month = data['month'] + 1 
            year = int(data['year'])
            account_id = ObjectId(session.get("account_id"))
            account = accounts.find_one({"_id": account_id})
            print(account)
            
            # Construct MongoDB query to filter documents based on month and year
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            start_date_iso = start_date.isoformat()
            end_date_iso = end_date.isoformat()

            query = {'CreatedDate': {'$gte': start_date_iso, '$lt': end_date_iso},
                     'Email': account['AccountOwner']['Email']}
            print(account['AccountOwner']['Email'])

            # Execute the query and convert the cursor to a list
            data_list = list(employees.find(query))
            print(data_list)
            
            if not data_list:
                print("No documents found for the given query.")
            # Convert MongoDB ObjectId to string
            for doc in data_list:
                doc['_id'] = str(doc['_id'])
            
            return jsonify(data_list), 200
        except KeyError:
            return jsonify({'error': 'Invalid input data. "month" and "year" are required.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Request does not contain JSON'}), 400
    
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
    

