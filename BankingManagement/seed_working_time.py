import random
from datetime import datetime, timedelta
import calendar
from models.database import Database
from models.working_day_info import WorkingDay
from enums.working_type import WorkingType
from enums.collection import CollectionType

def generate_fake_working_time():
    """Generate fake working time data for testing the interface"""
    print("Generating fake working time data...")
    
    # Connect to database
    db = Database().get_db()
    working_days_collection = db[CollectionType.WORKING_DAY_INFOS.value]
    
    # Clear existing working day records
    working_days_collection.delete_many({})
    print("Cleared existing working day records")
    
    # Get current date
    current_date = datetime.now()
    
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
            current_day = datetime(year, month, day)
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
                check_in = datetime(year, month, day, check_in_hour, check_in_minute)
                
                # Generate check-out time between 5:00 PM and 7:00 PM
                check_out_hour = random.randint(17, 18)
                check_out_minute = random.randint(0, 59)
                check_out = datetime(year, month, day, check_out_hour, check_out_minute)
                
                # Calculate total hours
                time_diff = check_out - check_in
                total_hours = round(time_diff.total_seconds() / 3600, 2)
                
            elif working_status == WorkingType.WFH.value:
                # Generate check-in time between 8:00 AM and 10:00 AM
                check_in_hour = random.randint(8, 9)
                check_in_minute = random.randint(0, 59)
                check_in = datetime(year, month, day, check_in_hour, check_in_minute)
                
                # Generate check-out time between 5:00 PM and 7:00 PM
                check_out_hour = random.randint(17, 18)
                check_out_minute = random.randint(0, 59)
                check_out = datetime(year, month, day, check_out_hour, check_out_minute)
                
                # Calculate total hours
                time_diff = check_out - check_in
                total_hours = round(time_diff.total_seconds() / 3600, 2)
            
            # Create working day record
            working_day = WorkingDay(
                emp_id=1,  # Assuming employee ID 1 exists
                day=day,
                month=month,
                year=year,
                workingStatus=working_status,
                checkIn=check_in,
                checkOut=check_out,
                totalHours=total_hours
            )
            
            # Save to database
            working_day.save()
    
    print(f"Generated fake working time data for the last 3 months")

if __name__ == "__main__":
    generate_fake_working_time() 