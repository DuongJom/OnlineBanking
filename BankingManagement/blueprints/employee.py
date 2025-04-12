from flask import Blueprint, render_template, request
from bson import ObjectId
from datetime import date, datetime as dt, timedelta
import random

from models.database import Database
from models.employee import Employee
from enums.month_type import MonthType
from enums.role_type import RoleType
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from enums.sex_type import SexType
from enums.working_type import WorkingType
from helpers.logger import log_request
from decorators import login_required, role_required

db = Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
employees = db[CollectionType.EMPLOYEES.value]
salaries = db[CollectionType.SALARIES.value]
roles = db[CollectionType.ROLES.value]
news = db[CollectionType.NEWS.value]

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
@login_required
@role_required(RoleType.EMPLOYEE.value)
@log_request()
def home():
    if request.method == 'GET':
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

def generate_fake_news(count=20):
    """Generate fake news data and insert into MongoDB"""
    
    # Sample data for random generation
    news_types = [
        {"type": 0, "name": "New", "bg_color": "green"},
        {"type": 1, "name": "Policy", "bg_color": "red"},
        {"type": 2, "name": "Event", "bg_color": "blue"},
        {"type": 3, "name": "Announcement", "bg_color": "orange"}
    ]
    
    titles = [
        "Company Policy Update",
        "New Work From Home Guidelines",
        "Annual Team Building Event",
        "Holiday Schedule Announcement",
        "New Employee Onboarding",
        "System Maintenance Notice",
        "Office Relocation Update",
        "New Project Launch",
        "Employee Benefits Update",
        "Security Protocol Changes",
        "Company Achievement Celebration",
        "New Feature Release",
        "Emergency Contact Update",
        "Training Program Schedule",
        "Performance Review Timeline",
        "New Department Structure",
        "Client Meeting Schedule",
        "Equipment Maintenance Notice",
        "New Software Implementation",
        "Office Safety Guidelines"
    ]
    
    contents = [
        "Important updates regarding company policies and procedures. Please review the new guidelines carefully.",
        "New work from home policy has been implemented. All employees are required to follow these guidelines.",
        "Join us for our annual team building event. All employees are welcome to participate.",
        "Updated holiday schedule for the upcoming months. Please check your calendar.",
        "Welcome to our new employees! Please complete the onboarding process.",
        "System maintenance scheduled for this weekend. Please save your work.",
        "Office relocation details and timeline. Please prepare accordingly.",
        "Exciting new project launch. Team members will be notified separately.",
        "Updates to employee benefits package. Please review the changes.",
        "New security protocols implemented. All employees must comply.",
        "Celebrating our company's recent achievements. Join us for the celebration.",
        "New features have been added to our system. Training will be provided.",
        "Please update your emergency contact information in the system.",
        "New training program schedule. All employees must complete the training.",
        "Performance review timeline announced. Please prepare your reports.",
        "New department structure implemented. Changes will take effect next month.",
        "Important client meeting schedule. All team members must attend.",
        "Equipment maintenance scheduled. Please backup your data.",
        "New software implementation timeline. Training will be provided.",
        "Updated office safety guidelines. All employees must follow these protocols."
    ]
    
    # Clear existing data (optional)
    news.delete_many({})
    
    # Generate current date for news dates
    current_date = dt.now()
    
    # Generate and insert fake news
    for i in range(count):
        # Generate random date within last 30 days
        days_ago = random.randint(0, 30)
        news_date = current_date - timedelta(days=days_ago)
        
        # Select random news type
        news_type = random.choice(news_types)
        
        # Create news document
        news_obj = {
            "_id": i+1,
            "Title": titles[i],
            "Content": contents[i],
            "Type": news_type["type"],
            "StartDate": news_date,
            "Status": random.randint(0, 1),  # 0: Unread, 1: Read
            "created_at": dt.now(),
            "updated_at": dt.now()
        }
        
        # Insert into MongoDB
        news.insert_one(news_obj)

@employee_blueprint.route('/employee/news', methods=['GET'])    
def show_news():
    generate_fake_news(20)
    lst_news = list(news.find())
    return render_template('employee/news.html', lnews=lst_news)