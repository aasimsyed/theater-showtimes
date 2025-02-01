"""Parses a file containing the hours of operation for a movie theater."""
from datetime import time
from typing import Dict, List, Tuple, Optional
from .utilities import weekdays, str_to_time

class TimeRange(Tuple[time, time]):
    """Represents a range of operating hours."""
    def __new__(cls, open_time: time, close_time: time) -> 'TimeRange':
        return super().__new__(cls, (open_time, close_time))

def parse_time_range(time_str: str) -> TimeRange:
    """
    Parse a time range string into open and close times.
    
    Args:
        time_str: String containing two times separated by " - " (e.g. "8:00am - 11:00pm")
        
    Returns:
        Tuple of (open_time, close_time)
        
    Raises:
        ValueError: If time format is invalid
    """
    try:
        open_str, close_str = [t.strip() for t in time_str.split(" - ")]
        return TimeRange(str_to_time(open_str), str_to_time(close_str))
    except ValueError as e:
        raise ValueError(f"Invalid time range format: {time_str}") from e

def extract_day_and_times(line: str) -> Tuple[str, TimeRange]:
    """
    Extract day part and time range from a line.
    
    Args:
        line: Line from hours file (e.g. "Monday - Wednesday 8:00am - 11:00pm")
        
    Returns:
        Tuple of (day_part, time_range)
        
    Raises:
        ValueError: If line format is invalid
    """
    try:
        # Find last occurrence of time pattern to split day and time parts
        time_parts = line.split(" - ")
        if len(time_parts) < 2:
            raise ValueError("Invalid hours format")
            
        # Parse times from end of line
        close_time = str_to_time(time_parts[-1].strip())
        open_time_part = time_parts[-2].strip()
        open_time = str_to_time(open_time_part.split()[-1])
        
        # Extract day part
        day_part = line[:line.rindex(open_time_part.split()[-1])].strip().rstrip("-").strip()
        
        # Validate day part contains valid day names
        day_words = [word.lower() for word in day_part.split()]
        if not any(day in weekdays for day in day_words):
            raise ValueError("Invalid hours format")
        
        return day_part, TimeRange(open_time, close_time)
    except (ValueError, IndexError) as e:
        raise ValueError("Invalid hours format") from e

def parse_hours_file(filename: str) -> Dict[str, TimeRange]:
    """
    Parse theater hours file and return a dictionary of day: (open_time, close_time).
    
    Args:
        filename: Path to the hours file
        
    Returns:
        Dictionary mapping days to time ranges
        
    Raises:
        ValueError: If the file format is invalid or file is empty
    """
    hours: Dict[str, TimeRange] = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Extract day part and times
                    day_part, time_range = extract_day_and_times(line)
                    
                    # Get list of days (handles ranges)
                    days = get_days_in_range(day_part) if " - " in day_part else [day_part]
                    
                    # Add hours for each day
                    for day in days:
                        hours[day] = time_range
                except ValueError as e:
                    raise ValueError("Invalid hours format") from e
                    
        if not hours:
            raise ValueError("No valid hours found in file")
            
        return hours
        
    except FileNotFoundError as e:
        raise ValueError(f"File not found: {filename}") from e

def get_days_in_range(day_range: str) -> List[str]:
    """Get list of days between start and end days inclusive."""
    try:
        if " - " in day_range:
            start_day, end_day = [d.strip() for d in day_range.split(" - ")]
        else:
            start_day = end_day = day_range.strip()
            
        # Validate day names
        if start_day.lower() not in weekdays or end_day.lower() not in weekdays:
            raise ValueError("Invalid hours format")
            
        start_idx = weekdays.index(start_day.lower())
        end_idx = weekdays.index(end_day.lower())
        
        if end_idx < start_idx:
            end_idx += 7
            
        return [weekdays[i % 7].capitalize() for i in range(start_idx, end_idx + 1)]
        
    except ValueError as e:
        raise ValueError("Invalid hours format") from e
