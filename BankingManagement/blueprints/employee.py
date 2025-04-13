import random
import calendar
import pandas as pd
import io
from flask import Blueprint, render_template, send_file, request, session
from bson import ObjectId
from datetime import date, datetime as dt, timedelta

from models.database import Database
from models.employee import Employee
from models.working_day_info import WorkingDay
from enums.month_type import MonthType
from enums.role_type import RoleType
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from enums.sex_type import SexType
from enums.working_type import WorkingType
from decorators import login_required, role_required, log_request
from helpers.helpers import get_max_id

db = Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
employees = db[CollectionType.EMPLOYEES.value]
salaries = db[CollectionType.SALARIES.value]
roles = db[CollectionType.ROLES.value]
news = db[CollectionType.NEWS.value]
working_day_infos = db[CollectionType.WORKING_DAY_INFOS.value]

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
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value)
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

def generate_fake_working_time():
    """Generate fake working time data for testing the interface"""
    
    # Clear existing working day records
    working_day_infos.delete_many({})
    
    # Get current date
    current_date = dt.now()
    
    # Generate data for the last 3 months
    for month_offset in range(3):
        # Calculate the month and year
        target_date = current_date - timedelta(days=30 * month_offset)
        year = target_date.year
        month = target_date.month
        
        # Get the number of days in the month
        _, days_in_month = calendar.monthrange(year, month)
        
        # Generate working day records for each day
        for day in range(1, days_in_month + 1):
            # Skip weekends (Saturday and Sunday)
            current_day = dt(year, month, day)
            if current_day.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
                continue
            
            # Randomly determine working status
            status_weights = [0.1, 0.2, 0.6, 0.1]  # Off, WFH, In Office, Other
            working_status = random.choices(
                [WorkingType.OFF.value, WorkingType.WFH.value, 
                 WorkingType.WORK_IN_COMPANY.value, WorkingType.OTHER.value],
                weights=status_weights
            )[0]
            
            # Generate check-in and check-out times based on working status
            check_in = None
            check_out = None
            total_hours = 0
            
            if working_status == WorkingType.WORK_IN_COMPANY.value:
                # Generate check-in time between 7:30 AM and 9:30 AM
                check_in_hour = random.randint(7, 9)
                check_in_minute = random.randint(0, 59) if check_in_hour == 7 else random.randint(0, 30)
                check_in = dt(year, month, day, check_in_hour, check_in_minute)
                
                # Generate check-out time between 5:00 PM and 7:00 PM
                check_out_hour = random.randint(17, 18)
                check_out_minute = random.randint(0, 59)
                check_out = dt(year, month, day, check_out_hour, check_out_minute)
                
                # Calculate total hours
                time_diff = check_out - check_in
                total_hours = round(time_diff.total_seconds() / 3600, 2)
                
            elif working_status == WorkingType.WFH.value:
                # Generate check-in time between 8:00 AM and 10:00 AM
                check_in_hour = random.randint(8, 9)
                check_in_minute = random.randint(0, 59)
                check_in = dt(year, month, day, check_in_hour, check_in_minute)
                
                # Generate check-out time between 5:00 PM and 7:00 PM
                check_out_hour = random.randint(17, 18)
                check_out_minute = random.randint(0, 59)
                check_out = dt(year, month, day, check_out_hour, check_out_minute)
                
                # Calculate total hours
                time_diff = check_out - check_in
                total_hours = round(time_diff.total_seconds() / 3600, 2)
            
            # Create working day record
            new_id = get_max_id(database=db, collection_name=CollectionType.WORKING_DAY_INFOS.value)
            working_day = WorkingDay(
                id=new_id,
                emp_id=1,
                day=day,
                month=month,
                year=year,
                workingStatus=working_status,
                checkIn=check_in,
                checkOut=check_out,
                totalHours=total_hours
            )
            
            # Save to database
            working_day_infos.insert_one(working_day.to_json())

@employee_blueprint.route('/employee/working-time', methods=['GET'])
@login_required
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value)
def working_time():
    if not session.get("account_id"):
        return None
        
    current_account = accounts.find_one({"_id": int(session.get("account_id"))})
    if not current_account:
        return None
        
    current_user = employees.find_one({"_id": int(current_account["AccountOwner"])})
    #generate_fake_working_time()

    # Get month parameter from request, default to current month
    month_param = request.args.get('month', None)
    
    if month_param:
        try:
            # Parse the month parameter (format: YYYY-MM)
            year, month = map(int, month_param.split('-'))
            current_date = dt(year, month, 1)
        except ValueError:
            # If invalid format, use current month
            current_date = dt.now()
    else:
        current_date = dt.now()
    
    # Get the first day of the month
    first_day = current_date.replace(day=1)
    
    # Get the last day of the month
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Get working day records for the current user in the selected month
    working_days = working_day_infos.find({
        'EmployeeId': 1,
        'Month': current_date.month,
        'Year': current_date.year
    })
    
    # Convert to dictionary for easier access
    working_days_dict = {day["Day"]: day for day in working_days}
    
    # Generate calendar days
    calendar_days = []
    working_days_count = 0
    half_days_count = 0
    day_offs_count = 0
    
    # Get the number of days in the month
    _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
    
    # Status counts for chart
    status_counts = [0] * 8  # 8 possible statuses (0-7)
    
    for day in range(1, days_in_month + 1):
        current_day = current_date.replace(day=day)
        
        # Check if it's a weekend
        is_weekend = current_day.weekday() >= 5
        
        # Get working day record for this day
        working_day = working_days_dict.get(day)
        
        # Determine working status
        working_status = WorkingType.OFF.value
        if working_day:
            working_status = working_day["WorkingStatus"]
        
        # Update counts
        if not is_weekend:
            if working_status == WorkingType.WORK_IN_COMPANY.value:
                working_days_count += 1
            elif working_status == WorkingType.HALF_DAY.value:
                half_days_count += 1
            elif working_status == WorkingType.OFF.value:
                day_offs_count += 1
            
            # Update status counts for chart
            status_counts[working_status] += 1
        
        calendar_days.append({
            'date': current_day.strftime('%d-%m-%Y'),
            'day_name': current_day.strftime('%A'),
            'working_status': working_status,
            'is_weekend': is_weekend
        })
    
    # Generate months for dropdown (last 12 months)
    months = []
    for i in range(12):
        date = dt.now() - timedelta(days=30*i)
        month_value = date.strftime('%Y-%m')
        month_label = date.strftime('%B %Y')
        is_selected = date.year == current_date.year and date.month == current_date.month
        
        months.append({
            'value': month_value,
            'label': month_label,
            'selected': is_selected
        })
    
    # Prepare chart data
    chart_data = {
        'data': status_counts
    }
    
    return render_template('employee/working_time.html',
                          calendar_days=calendar_days,
                          working_days=working_days_count,
                          half_days=half_days_count,
                          day_offs=day_offs_count,
                          months=months,
                          chart_data=chart_data)

@employee_blueprint.route('/employee/working-time/export', methods=['GET', 'POST'])
@login_required
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value)
def export_working_time():
    if not session.get("account_id"):
        return None
        
    current_account = accounts.find_one({"_id": int(session.get("account_id"))})
    if not current_account:
        return None
    
    # Get current user
    current_user = employees.find_one({"_id": int(current_account["AccountOwner"])})
    
    # Get month parameter from request, default to current month
    month_param = request.args.get('month', None)
    
    if month_param:
        try:
            # Parse the month parameter (format: YYYY-MM)
            year, month = map(int, month_param.split('-'))
            current_date = dt(year, month, 1)
        except ValueError:
            # If invalid format, use current month
            current_date = dt.now()
    else:
        current_date = dt.now()
    
    # Get working day records for the current user in the selected month
    working_days = working_day_infos.find({
        'EmployeeId': current_user['_id'],
        'Month': current_date.month,
        'Year': current_date.year
    })
    
    # Convert to list of dictionaries for DataFrame
    records_data = []
    
    # Get the number of days in the month
    _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
    
    # Create a dictionary of working days for easier access
    working_days_dict = {day.Day: day for day in working_days}
    
    # Status mapping
    status_mapping = {
        WorkingType.OFF.value: 'Off',
        WorkingType.HALF_DAY.value: 'Half Day',
        WorkingType.VACATION.value: 'Vacation',
        WorkingType.WEDDING.value: 'Wedding',
        WorkingType.SICK.value: 'Sick',
        WorkingType.WFH.value: 'WFH',
        WorkingType.WORK_IN_COMPANY.value: 'Work In Company',
        WorkingType.OTHER.value: 'Other'
    }
    
    for day in range(1, days_in_month + 1):
        current_day = current_date.replace(day=day)
        
        # Check if it's a weekend
        is_weekend = current_day.weekday() >= 5
        
        # Get working day record for this day
        working_day = working_days_dict.get(day)
        
        # Determine working status
        working_status = WorkingType.OFF.value
        if working_day:
            working_status = working_day.WorkingStatus
        
        # Get status text
        status_text = status_mapping.get(working_status, 'Other')
        if is_weekend:
            status_text = 'Weekend'
        
        records_data.append({
            'Date': current_day.strftime('%d-%m-%Y'),
            'Day': current_day.strftime('%A'),
            'Status': status_text
        })
    
    # Create DataFrame
    df = pd.DataFrame(records_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Working Time', index=False)
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Working Time']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Write the column headers with the header format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Set column widths
        worksheet.set_column('A:A', 12)  # Date
        worksheet.set_column('B:B', 10)  # Day
        worksheet.set_column('C:C', 15)  # Status
    
    # Seek to the beginning of the BytesIO object
    output.seek(0)
    
    # Generate filename
    filename = f"working_time_{current_date.strftime('%Y_%m')}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    ) 