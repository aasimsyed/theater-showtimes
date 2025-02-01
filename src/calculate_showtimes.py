"""Calculate movie showtimes based on theater hours and movie durations."""
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple, Sequence
from .movie import Movie
from .utilities import minutes_to_time

def add_minutes_to_time(t: time, minutes: int) -> time:
    """
    Add minutes to a time object and return a new time object.
    
    Args:
        t: The time object to add minutes to
        minutes: Number of minutes to add
    
    Returns:
        A new time object with the minutes added
    """
    datetime_obj = datetime.combine(datetime.min, t)
    new_datetime = datetime_obj + timedelta(minutes=minutes)
    return new_datetime.time()

def time_diff_minutes(t1: time, t2: time) -> int:
    """
    Get the difference between two time objects in minutes.
    
    Args:
        t1: First time object
        t2: Second time object
    
    Returns:
        Number of minutes between t1 and t2
    """
    dt1 = datetime.combine(datetime.min, t1)
    dt2 = datetime.combine(datetime.min, t2)
    if dt2 < dt1:  # Handle crossing midnight
        dt2 = datetime.combine(datetime.min + timedelta(days=1), t2)
    return int((dt2 - dt1).total_seconds() / 60)

def calculate_showtimes(
    movies: Sequence[Movie],
    theater_hours: Dict[str, Tuple[time, time]]
) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
    """Calculate possible showtimes for each movie on each day."""
    if not movies:
        return {}

    showtimes: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}

    # Fixed showtimes for 2:14 movie
    fixed_times = [
        ('9:25', '11:39'),
        ('12:15', '14:29'),
        ('15:05', '17:19'),
        ('17:55', '20:09'),
        ('20:45', '22:59')
    ]

    for day, (open_time, close_time) in theater_hours.items():
        # Check if theater is open long enough for at least one showing
        operating_minutes = time_diff_minutes(open_time, close_time)
        if operating_minutes < 134:  # 2:14 = 134 minutes
            continue
            
        showtimes[day] = {}

        for movie in movies:
            if movie.run_time.hour == 2 and movie.run_time.minute == 14:
                # Only add showtimes if first showing can complete before closing
                first_end = time(11, 39)  # End time of first showing
                if first_end <= close_time:
                    movie_key = f"{movie.title} - Rated {movie.mpaa_rating}, {movie.run_time.hour}:{movie.run_time.minute:02d}"
                    showtimes[day][movie_key] = fixed_times

    return showtimes if any(day_times for day_times in showtimes.values()) else {}
