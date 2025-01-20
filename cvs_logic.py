import os
import csv
import datetime


# START_TIME = datetime.time(8, 0)  # 8:00 AM
# LATE_THRESHOLD = datetime.timedelta(minutes=45)
# COOLDOWN_PERIOD = datetime.timedelta(seconds=30)  # 30-second cooldown

# Directory to store daily attendance logs (same as source folder)
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


