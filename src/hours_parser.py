"""Parses a file containing the hours of operation for a movie theater."""
from datetime import time
from typing import Dict, List, Tuple, Optional
from .utilities import weekdays, str_to_time

class TimeRange(Tuple[time, time]):
    """Represents a range of operating hours."""
    def __new__(cls, open_time: time, close_time: time) -> 'TimeRange':
        return super().__new__(cls, (open_time, close_time))

def parse_time_range(time_str: str) -> TimeRange:
    """Parse a time range string into open and close times."""
    try:
        # Handle both formats: "8:00am - 11:00pm" and "8:00am-11:00pm"
        time_str = time_str.replace(' ', '')
        open_str, close_str = [t.strip() for t in time_str.split('-')]
        return TimeRange(str_to_time(open_str), str_to_time(close_str))
    except ValueError as exc:
        raise ValueError(f"Invalid time range format: {time_str}") from exc

def extract_day_and_times(line: str) -> Tuple[str, TimeRange]:
    """Extract day part and time range from a line."""
    try:
        # Split on " - " to handle day ranges and time ranges
        parts = [p.strip() for p in line.split(' - ')]
        
        if len(parts) == 3:  # Day range: "Monday - Wednesday 8:00am - 11:00pm"
            day_part = f"{parts[0]} - {parts[1]}"
            time_range = parse_time_range(parts[2])
        elif len(parts) == 2:  # Single day: "Monday 8:00am - 11:00pm"
            # Check if first part contains a time
            if any(c.isdigit() for c in parts[0]):
                day_part = parts[0].split()[0]
                time_range = parse_time_range(f"{parts[0].split()[-1]}-{parts[1]}")
            else:
                day_part = parts[0]
                time_range = parse_time_range(parts[1])
        else:
            raise ValueError("Invalid format")
        
        # Validate day names
        day_words = [w.strip().lower() for w in day_part.split('-')]
        if not all(d.strip() in weekdays for d in day_words if d.strip()):
            raise ValueError("Invalid day name")
            
        return day_part, time_range
        
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Invalid line format: {line}") from exc

def get_days_in_range(day_part: str) -> List[str]:
    """Get list of days in a range."""
    days = [d.strip() for d in day_part.split('-')]
    if len(days) == 1:
        return [days[0]]
        
    start_idx = weekdays.index(days[0].lower())
    end_idx = weekdays.index(days[1].lower())
    
    if start_idx <= end_idx:
        return [d.capitalize() for d in weekdays[start_idx:end_idx + 1]]
    else:
        # Handle wrapping around the week
        return ([d.capitalize() for d in weekdays[start_idx:]] + 
                [d.capitalize() for d in weekdays[:end_idx + 1]])

def parse_hours_file(filename: str) -> Dict[str, TimeRange]:
    """Parse theater hours file."""
    hours: Dict[str, TimeRange] = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    day_part, time_range = extract_day_and_times(line)
                    days = get_days_in_range(day_part) if '-' in day_part else [day_part]
                    
                    for day in days:
                        hours[day.capitalize()] = time_range
                        
                except ValueError as e:
                    print(f"Warning: Skipping invalid line '{line}': {str(e)}")
                    
        if not hours:
            raise ValueError("No valid hours found in file")
            
        return hours
        
    except FileNotFoundError as exc:
        raise ValueError(f"Hours file not found: {filename}") from exc
