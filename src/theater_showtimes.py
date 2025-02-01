#!/usr/bin/env python3
"""Main module for the theater showtimes program."""
import sys
import os
from .movie_list_parser import parse_movie_list
from .hours_parser import parse_hours_file
from .calculate_showtimes import calculate_showtimes
from .display_showtimes import display_showtimes
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class TheaterShowtimes:
    def __init__(self):
        self.CLEANUP_TIME = timedelta(minutes=30)  # Standard cleanup time between shows
        self.days_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }

    def parse_time(self, time_str: str) -> datetime:
        """Convert time string to datetime object"""
        try:
            # Handle both 12-hour and 24-hour formats
            for fmt in ['%I:%M%p', '%H:%M']:
                try:
                    return datetime.strptime(time_str.strip(), fmt)
                except ValueError:
                    continue
            raise ValueError(f"Invalid time format: {time_str}")
        except Exception as e:
            raise ValueError(f"Error parsing time: {time_str}") from e

    def parse_operating_hours(self, hours_text: str) -> Dict[str, Tuple[datetime, datetime]]:
        """Parse operating hours text into structured format"""
        operating_hours = {}
        for line in hours_text.strip().split('\n'):
            days, hours = line.split(' ', 1)
            days = [d.strip() for d in days.split('-')]
            
            # Parse start and end times
            start_time, end_time = hours.split('-')
            start_dt = self.parse_time(start_time)
            end_dt = self.parse_time(end_time)
            
            # Handle day ranges
            if len(days) == 2:
                start_day, end_day = days
                current_day = start_day
                while True:
                    operating_hours[current_day.strip()] = (start_dt, end_dt)
                    if current_day == end_day:
                        break
                    current_day = list(self.days_map.keys())[
                        (self.days_map[current_day] + 1) % 7
                    ]
            else:
                operating_hours[days[0].strip()] = (start_dt, end_dt)
                
        return operating_hours

    def calculate_showtimes(self, 
                          movies: List[Dict], 
                          operating_hours: Dict[str, Tuple[datetime, datetime]], 
                          day: str) -> List[Dict]:
        """Calculate optimal showtimes for given movies on specified day"""
        if day not in operating_hours:
            raise KeyError(f"No operating hours defined for {day}")

        start_time, end_time = operating_hours[day]
        showtimes = []
        
        # Use a reference date for all calculations to ensure proper time arithmetic
        ref_date = start_time.date()
        current_datetime = start_time

        # Sort movies by runtime for optimal packing
        sorted_movies = sorted(movies, key=lambda x: self.parse_runtime(x['Run Time']))

        while current_datetime < end_time:
            shortest_movie = sorted_movies[0]
            shortest_runtime = self.parse_runtime(shortest_movie['Run Time'])
            
            # If we can't even fit the shortest movie, break
            potential_end = current_datetime + shortest_runtime + self.CLEANUP_TIME
            if potential_end > end_time:
                break

            # Try to schedule each movie
            for movie in sorted_movies:
                runtime = self.parse_runtime(movie['Run Time'])
                movie_end_datetime = current_datetime + runtime
                cleanup_end_datetime = movie_end_datetime + self.CLEANUP_TIME

                # Check if movie plus cleanup fits before closing
                if cleanup_end_datetime <= end_time:
                    showtimes.append({
                        'movie': movie['Movie Title'],
                        'start_time': current_datetime.strftime('%I:%M %p'),
                        'end_time': movie_end_datetime.strftime('%I:%M %p')
                    })
                    
                    # Move current time to after cleanup period
                    current_datetime = cleanup_end_datetime
                    break
            else:
                # If no movie could be scheduled, increment by 15 minutes
                current_datetime = current_datetime + timedelta(minutes=15)
                if current_datetime >= end_time:
                    break

        return showtimes

    def parse_runtime(self, runtime: str) -> timedelta:
        """Convert runtime string to timedelta"""
        try:
            hours, minutes = map(int, runtime.split(':'))
            return timedelta(hours=hours, minutes=minutes)
        except Exception as e:
            raise ValueError(f"Invalid runtime format: {runtime}") from e

def main():
    """Main function for the theater showtimes program."""
    if len(sys.argv) != 2:
        print("Usage: ./theater_showtimes.py <movie_list_file>")
        sys.exit(1)

    movie_list_file = sys.argv[1]
    hours_file = os.path.join(os.path.dirname(__file__), "..", "resources", "hours.txt")

    try:
        # Parse input files
        movies = parse_movie_list(movie_list_file)
        hours = parse_hours_file(hours_file)
        
        # Calculate and display showtimes
        showtimes = calculate_showtimes(movies, hours)
        display_showtimes(showtimes)
        
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
