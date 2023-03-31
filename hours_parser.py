import calendar
from datetime import datetime
from utilities import weekdays

HOURS_ERROR = "Invalid line format. Example of valid format: 'Monday - Wednesday 8:00am - 11:00pm' or 'Thursday 8:00am - 11:00pm'"

def parse_hours_file(hours_file):
    hours = {}

    with open(hours_file, "r") as file:
        lines = file.readlines()

        for line in lines:
            try:
                line = line.strip().lower()
                parts = line.split()

                if len(parts) != 4 and len(parts) != 6:
                    raise ValueError(HOURS_ERROR)

                if "-" not in parts[1:3]:
                    raise ValueError(HOURS_ERROR)

                start_day, end_day = None, None

                if len(parts) == 4:
                    start_day = end_day = parts[0]
                elif len(parts) == 6:
                    start_day = parts[0]
                    end_day = parts[2]
                else:
                    raise ValueError(HOURS_ERROR)

                if start_day not in weekdays:
                    raise ValueError(f"Invalid day: {start_day}")
                if end_day not in weekdays:
                    raise ValueError(f"Invalid day: {end_day}")

                start_index = weekdays.index(start_day)
                end_index = weekdays.index(end_day) + 1

                if start_index >= end_index:
                    end_index += len(weekdays)

                days = [calendar.day_name[i % 7].capitalize() for i in range(start_index, end_index)]

                start_time, end_time = parts[-3], parts[-1]

                start_time_obj = datetime.strptime(start_time, "%I:%M%p").time()
                end_time_obj = datetime.strptime(end_time, "%I:%M%p").time()

                if start_time_obj > end_time_obj:
                    raise ValueError("Start time must be before end time")

                for day in days:
                    hours[day.capitalize()] = (start_time_obj, end_time_obj)
            except ValueError as e:
                print(f"Error processing line: {line}. {e}")

    return hours
