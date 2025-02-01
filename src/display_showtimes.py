"""Displays the showtimes for today's movies."""

from datetime import time
from typing import Dict, List

def display_showtimes(showtimes: Dict[str, Dict[str, List[time]]]) -> None:
    """
    Display the calculated showtimes in a formatted way.
    
    Args:
        showtimes: Dictionary mapping days to dictionaries of movie titles to lists of showtime start times
    """
    if not showtimes:
        print("No showtimes available.")
        return
        
    for day, movies in sorted(showtimes.items()):
        print(f"\n{day}:")
        for movie, times in sorted(movies.items()):
            time_strs = [t.strftime("%I:%M %p") for t in sorted(times)]
            print(f"  {movie}:")
            print(f"    {', '.join(time_strs)}")
