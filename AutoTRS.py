import calendar
import os
import subprocess
from datetime import date, timedelta

def get_current_year_month():
    year = date.today().year
    month = date.today().month
    return year, month

def get_weekday_dates(year, month, work_days, cut_off_day):
    total_days = calendar.monthrange(year, month)[1]
    weekday_dates = [date(year, month, day) for day in range(1, total_days + 1) if date(year, month, day).weekday() in work_days and day <= cut_off_day]
    return [current_date.strftime("%m-%d-%Y") for current_date in weekday_dates]

def pad_time(time):
    return "0" + time if len(time) == 7 else time

def append_start_end_time(weekday_dates, start_time, end_time):
    start_time = pad_time(start_time)
    end_time = pad_time(end_time)
    return [date + " " + start_time for date in weekday_dates], [date + " " + end_time for date in weekday_dates]

def calculate_hours_worked(start_time, end_time):
    start_hour = start_time[11:19]
    end_hour = end_time[11:19]

    if start_hour[-2:] == "PM":
        start_hour = str(int(start_hour[:2]) + 12) + start_hour[2:]
    if end_hour[-2:] == "PM":
        end_hour = str(int(end_hour[:2]) + 12) + end_hour[2:]

    return int(end_hour[:2]) - int(start_hour[:2])

def create_csv(weekday_dates_start, weekday_dates_end, hours_worked, csv_file_path):
    with open(csv_file_path, "w") as file:
        for i in range(len(weekday_dates_start)):
            file.write(weekday_dates_start[i] + "\n")
            file.write(weekday_dates_end[i] + "\n")
            file.write(str(hours_worked) + "\n")

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    year, month = get_current_year_month()
    
    work_days_input = input("Enter the days of the week you work (e.g. Mon,Tue,Wed,Thu,Fri): ")
    work_days_dict = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    work_days = [work_days_dict[day.strip()] for day in work_days_input.split(',')]

    cut_off_day = int(input("What is the last day you want to fill in for your time sheet? Put 0 for the last day of the month. "))
    if cut_off_day == 0:
        cut_off_day = calendar.monthrange(year, month)[1]

    weekday_dates = get_weekday_dates(year, month, work_days, cut_off_day)

    start_time = input("What time do you start work? (e.g. 11:00 AM) ")
    end_time = input("What time do you end work? (e.g. 04:00 PM) ")

    weekday_dates_start, weekday_dates_end = append_start_end_time(weekday_dates, start_time, end_time)

    hours_worked = calculate_hours_worked(weekday_dates_start[0], weekday_dates_end[0])

    input_data_directory = os.path.join(script_directory, "input")
    if not os.path.exists(input_data_directory):
        os.makedirs(input_data_directory)

    csv_file_path = os.path.join(input_data_directory, "input.csv")
    create_csv(weekday_dates_start, weekday_dates_end, hours_worked, csv_file_path)
   
    input("Please open Firefox and the TRS window and then press enter.")

    # Get path to ahk exe file
    ahk_file_directory = os.path.join(script_directory, "ahk")
    ahk_file_path = os.path.join(ahk_file_directory, "AutoTRS.exe")

    # call the AHK executable with any necessary arguments
    subprocess.call(ahk_file_path)

if __name__ == "__main__":
    main()