import csv
import calendar
from datetime import datetime, timedelta

weekdays = [day.lower() for day in calendar.day_name]

def is_valid_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            return True
    except (csv.Error, FileNotFoundError):
        return False
    
def time_to_minutes(time_obj):
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}:{remaining_minutes:02d}"