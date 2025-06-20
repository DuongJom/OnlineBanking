import random
import calendar
import pandas as pd
import io
from flask import Blueprint, render_template, send_file, request, session
from bson import ObjectId
from datetime import date, datetime as dt, timedelta

from models.employee import Employee
from enums.month_type import MonthType
from enums.role_type import RoleType
from enums.deleted_type import DeletedType
from enums.sex_type import SexType
from enums.working_type import WorkingType
from decorators import login_required, role_required, log_request
from helpers.helpers import get_max_id
from init_database import (
    db, accounts, employees, salaries, roles, news, working_day_infos
)

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
    all_employees = list(employees.find({"IsDeleted": DeletedType.AVAILABLE.value}))
    for employee in all_employees:
        employee['_id'] = int(employee['_id'])

    logged_in_user = Employee(
        id=1,
        employeeName=f"Employee 1",
        position="Junior Developer",
        role=RoleType.EMPLOYEE.value,
        sex=SexType.MALE.value,
        phone=f"0{random.randint(100000000, 999999999)}",
        email=f"employee1@dhcbank.com",
        address=f"Street {random.randint(1, 100)}, City {random.randint(1, 10)}",
        checkIn="08:00",
        checkOut="17:00",
        workingStatus=WorkingType.WORK_IN_COMPANY.value
    )
    return render_template('employee/home.html',
                           employees=all_employees,
                           is_checked_in=True,
                           is_checked_out=True,
                           emp=logged_in_user,
                           work_time=8)


@employee_blueprint.route('/employee/news', methods=['GET'])
def show_news():
    lst_news = list(news.find())
    return render_template('employee/news.html', lnews=lst_news)


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
    total_hours_in_month = 0
    
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
        check_in_time = None
        check_out_time = None
        total_hours = 0

        if working_day:
            working_status = working_day["WorkingStatus"]
            if working_day["CheckIn"]:
                check_in_time = dt.strptime(working_day["CheckIn"], '%Y-%m-%dT%H:%M:%S')
            if working_day["CheckOut"]:
                check_out_time = dt.strptime(working_day["CheckOut"], '%Y-%m-%dT%H:%M:%S')
            if working_day["TotalHours"]:
                total_hours = working_day["TotalHours"]
        
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
            total_hours_in_month += total_hours
        
        calendar_days.append({
            'date': current_day.strftime('%d-%m-%Y'),
            'day_name': current_day.strftime('%A'),
            'working_status': working_status,
            'is_weekend': is_weekend,
            'check_in': check_in_time,
            'check_out': check_out_time,
            'total_hours': total_hours
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
    
    return render_template('employee/working_time.html',
                          calendar_days=calendar_days,
                          working_days=working_days_count,
                          half_days=half_days_count,
                          day_offs=day_offs_count,
                          total_hours_in_month=total_hours_in_month,
                          months=months)

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
    
    for day in range(1, days_in_month + 1):
        current_day = current_date.replace(day=day)
        
        # Check if it's a weekend
        is_weekend = current_day.weekday() >= 5
        
        # Get working day record for this day
        working_day = working_days_dict.get(day)
        status_text = WorkingType.OFF.name.capitalize()  # Default status

        # Determine working status
        working_status = WorkingType.OFF.value
        if working_day:
            working_status = working_day.WorkingStatus

        match working_status:
            case WorkingType.OFF.value:
                status_text = WorkingType.OFF.name.capitalize()
            case WorkingType.HALF_DAY.value:
                status_text = WorkingType.HALF_DAY.name.capitalize()
            case WorkingType.VACATION.value:
                status_text = WorkingType.VACATION.name.capitalize()
            case WorkingType.WEDDING.value:
                status_text = WorkingType.WEDDING.name.capitalize()
            case WorkingType.SICK.value:
                status_text = WorkingType.SICK.name.capitalize()
            case WorkingType.WFH.value:
                status_text = WorkingType.WFH.name.capitalize()
            case WorkingType.WORK_IN_COMPANY.value:
                status_text = WorkingType.WORK_IN_COMPANY.name.capitalize()
            case WorkingType.OTHER.value:
                status_text = WorkingType.OTHER.name.capitalize()

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