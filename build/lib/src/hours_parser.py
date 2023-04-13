"""Parses a file containing the hours of operation for a movie theater."""
import calendar
from utilities import weekdays, str_to_time

HOURS_ERROR = ("Invalid line format. Example of valid format: "
               "'Monday - Wednesday 8:00am - 11:00pm' or "
               "'Thursday 8:00am - 11:00pm'")

def parse_days_and_times(parts):
    """Parses the days and times from a line in the hours file."""
    if len(parts) == 4:
        start_day = end_day = parts[0]
    elif len(parts) == 6:
        start_day = parts[0]
        end_day = parts[2]
    else:
        raise ValueError(HOURS_ERROR)

    start_time, end_time = parts[-3], parts[-1]
    return start_day, end_day, start_time, end_time


def validate_parts(parts):
    """Validates the parts of a line in the hours file."""
    if len(parts) != 4 and len(parts) != 6:
        raise ValueError(HOURS_ERROR)

    if "-" not in parts[1:3]:
        raise ValueError(HOURS_ERROR)


def get_day_indexes(start_day, end_day):
    """Gets the indexes of the start and end days."""
    start_index = weekdays.index(start_day)
    end_index = weekdays.index(end_day) + 1

    if start_index >= end_index:
        end_index += len(weekdays)

    return start_index, end_index


def get_days_and_times(parts):
    """Gets the days and times from the parts of a line in the hours file."""
    days_and_times = parse_days_and_times(parts)
    start_day, end_day = days_and_times[:2]
    start_time, end_time = days_and_times[2:]
    return start_day, end_day, start_time, end_time

def process_days_and_hours(hours, start_day, end_day, start_time_obj, end_time_obj):
    """Processes the days and hours and adds them to the hours dictionary."""
    start_index, end_index = get_day_indexes(start_day, end_day)
    days = [calendar.day_name[i % 7].capitalize() for i in range(start_index, end_index)]

    for day in days:
        hours[day.capitalize()] = (start_time_obj, end_time_obj)

def parse_hours_file(hours_file):
    """Parses the hours file and returns a dictionary of hours."""
    hours = {}

    with open(hours_file, "r", encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            try:
                line = line.strip().lower()
                parts = line.split()
                validate_parts(parts)

                start_day, end_day, start_time, end_time = get_days_and_times(parts)
                start_time_obj = str_to_time(start_time)
                end_time_obj = str_to_time(end_time)

                if start_time_obj > end_time_obj:
                    raise ValueError("Start time must be before end time")

                process_days_and_hours(hours, start_day, end_day, start_time_obj, end_time_obj)

            except ValueError as error:
                print(f"Error processing line: {line}. {error}")

    return hours
