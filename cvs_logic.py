import os
import csv
import datetime


# START_TIME = datetime.time(8, 0)  # 8:00 AM
# LATE_THRESHOLD = datetime.timedelta(minutes=45)
# COOLDOWN_PERIOD = datetime.timedelta(seconds=30)  # 30-second cooldown

# Directory to store daily attendance logs (same as source folder)
def load_attendance_log():
    """
    Reads the current day's attendance log file and updates the employee_status and last_clock_in_date.
    """
    log_filename = get_daily_log_filename()
    if not os.path.isfile(log_filename):
        return {}, {}  # No log file yet; return empty dictionaries

    employee_status = {}
    last_clock_in_date = {}

    with open(log_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employee_id = row["EmployeeID"]
            date = row["Date"]
            status = row["Status"]
            
            # Update employee status and last clock-in date
            if "Clocking In" in status:
                employee_status[employee_id] = "Clocked In"
                last_clock_in_date[employee_id] = date
            elif "Clocking Out" in status:
                employee_status[employee_id] = "Clocked Out"
    
    return employee_status, last_clock_in_date

log_directory = os.getcwd()  # Get the current working directory (script location)

def get_daily_log_filename():
    """
    Generates the log filename for the current day in the source folder.
    """
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")  # Format date as day-month-year
    return os.path.join(log_directory, f"attendance_log_{current_date}.csv")


def write_to_csv(employeeIds, date, time, status):
    """
    Writes matched employee's details into the daily CSV file.
    """
    log_filename = get_daily_log_filename()
    file_exists = os.path.isfile(log_filename)

    with open(log_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header only if the file is being created for the first time
        if not file_exists:
            writer.writerow(["EmployeeID", "Date", "Time", "Status"])
        writer.writerow([employeeIds, date, time, status])
    print(f"Logged: {employeeIds} - {date} {time} ({status})")


