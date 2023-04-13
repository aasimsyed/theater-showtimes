"""This module contains utility functions for the project."""
import csv
import calendar
from datetime import datetime

# Get a list of the days of the week
weekdays = [day.lower() for day in calendar.day_name]

def is_valid_csv(file_path):
    """Returns True if the file is a valid movie list CSV file, False otherwise."""
    required_columns = {"Movie Title", "Release Year", "MPAA Rating", "Run Time"}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            header = set(reader.fieldnames)
            if header != required_columns:
                raise ValueError(f"{file_path} is not a valid movie list CSV file")
            csv.Sniffer().sniff(file.read(1024))
            return True
    except (csv.Error, ValueError) as error:
        raise ValueError(f"{file_path} is not a valid movie list CSV file") from error

def time_to_minutes(time_obj):
    """Converts a datetime.time object to minutes."""
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    """Converts minutes to a datetime.time object."""
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}:{remaining_minutes:02d}"

def str_to_time(time_str):
    """Parses a string in the format HH:MMam/pm and returns a datetime.time object."""
    return datetime.strptime(time_str, '%I:%M%p').time()

def parse_run_time(run_time_str):
    """Parses a string in the format HH:MM and returns a datetime.time object."""
    return datetime.strptime(run_time_str.strip(), "%I:%M").time()
