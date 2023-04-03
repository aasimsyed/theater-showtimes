"""This module contains utility functions for the project."""
import os
import csv
import calendar
from datetime import datetime

weekdays = [day.lower() for day in calendar.day_name]

def is_valid_csv(file_path):
    """Returns True if the file is a valid CSV file, False otherwise."""
    try:
        if not os.path.isfile(file_path):
            raise ValueError(f"{file_path} does not exist or is not a file")
        with open(file_path, 'r', encoding="utf-8") as file:
            csv.Sniffer().sniff(file.read(1024))
            return True
    except (csv.Error, ValueError, IsADirectoryError) as error:
        raise ValueError(f"{file_path} is not a valid CSV file") from error


def time_to_minutes(time_obj):
    """Converts a datetime.time object to minutes."""
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    """Converts minutes to a datetime.time object."""
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}:{remaining_minutes:02d}"

# Convert a string in the format "8:00am" to a time object
def str_to_time(time_str):
    return datetime.strptime(time_str, '%I:%M%p').time()

def parse_run_time(run_time_str):
    """Parses a string in the format HH:MM and returns a datetime.time object."""
    return datetime.strptime(run_time_str.strip(), "%I:%M").time()
