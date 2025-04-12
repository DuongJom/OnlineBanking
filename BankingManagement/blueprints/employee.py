from flask import Blueprint, render_template, request, jsonify, session
from bson import ObjectId
from datetime import datetime, date

from models.database import Database
from models.employee import Employee

from helpers.helpers import paginator
from datetime import datetime, date
from helpers.logger import log_request
from decorators import login_required, role_required
from enums.month_type import MonthType
from enums.role_type import RoleType
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from enums.sex_type import SexType
from enums.working_type import WorkingType

db = Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
employees = db[CollectionType.EMPLOYEES.value]
salaries = db[CollectionType.SALARIES.value]
roles = db[CollectionType.ROLES.value]

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

import random
from datetime import timedelta
def generate_fake_employees(count=100):
    
    # Sample data for random generation
    positions = [
        "CEO", "CTO", "CFO", "COO", "Manager", 
        "Senior Developer", "Junior Developer", 
        "Senior Designer", "Junior Designer",
        "HR Manager", "HR Staff",
        "Senior Accountant", "Junior Accountant",
        "Sales Manager", "Sales Representative",
        "Marketing Manager", "Marketing Specialist",
        "Customer Service", "IT Support",
        "Project Manager", "Business Analyst"
    ]
    
    sexes = ["Male", "Female"]
    working_statuses = ["Active", "On Leave", "WFH", "Remote"]
    
    # Generate current date for working days
    current_date = datetime.now()
    
    # Clear existing data (optional)
    employees.delete_many({})
    
    # Generate and insert fake employees
    for i in range(count):
        # Generate random working days (last 30 days)
        working_days = []
        day_offs = []
        for day in range(30):
            date = current_date - timedelta(days=day)
            if random.random() < 0.8:  # 80% chance of working
                working_days.append(date.strftime("%Y-%m-%d"))
            else:
                day_offs.append(date.strftime("%Y-%m-%d"))
        
        # Generate random check-in/out times
        check_in_hour = random.randint(7, 9)
        check_out_hour = random.randint(17, 19)
        
        employee = {
            "_id": (i + 1),
            "EmployeeName": f"Employee {i+1}",
            "Position": random.choice(positions),
            "Role": RoleType.EMPLOYEE.value,
            "Sex": random.choice(sexes),
            "Phone": f"0{random.randint(100000000, 999999999)}",
            "Email": f"employee{i+1}@dhcbank.com",
            "Address": f"Street {random.randint(1, 100)}, City {random.randint(1, 10)}",
            "Check_in_time": f"{check_in_hour:02d}:00",
            "Check_out_time": f"{check_out_hour:02d}:00",
            "Working_status": random.choice(working_statuses),
            "Working_days": working_days,
            "DayOffs": day_offs,
            "Salary": random.randint(5000000, 20000000),
            "IsDeleted": DeletedType.AVAILABLE.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Insert into MongoDB
        employees.insert_one(employee)

@employee_blueprint.route('/employee/home', methods = ['GET'])
@login_required
@role_required(RoleType.EMPLOYEE.value)
@log_request()
def employee_home():
    if request.method == 'GET':
        #generate_fake_employees(50)
        all_employees = list(employees.find({ "IsDeleted": DeletedType.AVAILABLE.value }))
        for employee in all_employees:
            employee['_id'] = int(employee['_id'])

        logged_in_user = Employee(
            id = 1,
            employeeName=f"Employee 1",
            position = "Junior Developer",
            role = RoleType.EMPLOYEE.value,
            sex = SexType.MALE.value,
            phone = f"0{random.randint(100000000, 999999999)}",
            email = f"employee1@dhcbank.com",
            address = f"Street {random.randint(1, 100)}, City {random.randint(1, 10)}",
            checkIn = "08:00",
            checkOut = "17:00",
            workingStatus = WorkingType.WORK_IN_COMPANY.value
        )
        return render_template('employee/home.html', 
                               employees=all_employees, 
                               is_checked_in=True, 
                               is_checked_out=True,
                               emp=logged_in_user,
                               work_time=8)

@employee_blueprint.route('/employee/news', methods=['GET'])    
def news():
    return render_template('employee/news.html')