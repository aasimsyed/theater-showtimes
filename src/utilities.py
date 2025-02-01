"""Utility functions for the theater showtimes application."""
from datetime import datetime, time
from typing import List

# List of weekdays starting with Monday
weekdays: List[str] = [
    "monday", "tuesday", "wednesday", "thursday", 
    "friday", "saturday", "sunday"
]

def str_to_time(time_str: str) -> time:
    """
    Convert a string in format '8:00am' to a time object.
    
    Args:
        time_str: Time string in 12-hour format (e.g., '8:00am' or '8:00 am')
        
    Returns:
        datetime.time object
        
    Raises:
        ValueError: If the time format is invalid
    """
    try:
        # Extract just the time part if day is included
        if any(day.lower() in time_str.lower() for day in weekdays):
            time_str = time_str.split(" ")[-1]
            
        # Handle both formats: "8:00am" and "8:00 am"
        time_str = time_str.strip().replace(" ", "")
        return datetime.strptime(time_str, "%I:%M%p").time()
    except ValueError as e:
        raise ValueError(f"Invalid time format: {time_str}") from e

def time_to_minutes(t: time) -> int:
    """
    Convert a time object to minutes since midnight.
    
    Args:
        t: Time object to convert
        
    Returns:
        Number of minutes since midnight
    """
    return t.hour * 60 + t.minute

def minutes_to_time(minutes: int) -> time:
    """
    Convert minutes since midnight to a time object.
    
    Args:
        minutes: Number of minutes since midnight
        
    Returns:
        datetime.time object
    """
    # Handle wrapping around midnight
    minutes = minutes % (24 * 60)  # Wrap to 24-hour period
    hours = minutes // 60
    mins = minutes % 60
    return time(hour=hours, minute=mins)
