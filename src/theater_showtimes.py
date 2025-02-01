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
            # Normalize the time string
            time_str = time_str.strip().lower().replace(' ', '')
            
            # Handle various time formats
            formats = [
                '%I:%M%p',    # 9:00am
                '%I:%M%p',    # 9:00 am (spaces already removed)
                '%H:%M',      # 09:00 (24-hour)
            ]
            
            # Try each format
            for fmt in formats:
                try:
                    # Use today's date for the datetime
                    return datetime.combine(
                        datetime.today().date(),
                        datetime.strptime(time_str, fmt).time()
                    )
                except ValueError:
                    continue
                
            raise ValueError(f"Time must be in format HH:MMam/pm or HH:MM (24-hour)")
        
        except Exception as exc:
            raise ValueError(f"Invalid time format '{time_str}'. Use format like '9:00am' or '21:00'") from exc

    def parse_operating_hours(self, hours_text: str) -> Dict[str, Tuple[datetime, datetime]]:
        """Parse operating hours text into structured format"""
        operating_hours = {}
        
        for line in hours_text.strip().split('\n'):
            if not line.strip():
                continue
            
            try:
                # Split into days and hours parts
                parts = line.strip().split(' ')
                if len(parts) == 6:  # Day range format: "Monday - Friday 9:00am - 11:30pm"
                    days = [parts[0], parts[2]]
                    start_time, end_time = parts[3], parts[5]
                elif len(parts) == 4:  # Single day format: "Monday 9:00am - 11:30pm"
                    days = [parts[0]]
                    start_time, end_time = parts[1], parts[3]
                else:
                    raise ValueError("Invalid format. Expected format: 'Day - Day HH:MMam - HH:MMpm' or 'Day HH:MMam - HH:MMpm'")
                
                # Parse the times - split on last occurrence of ' - ' for times
                try:
                    start_dt = self.parse_time(start_time)
                    end_dt = self.parse_time(end_time)
                except ValueError as e:
                    raise ValueError(f"Invalid time format: {start_time} or {end_time}") from e
                
                # Handle day ranges
                if len(days) == 2:
                    start_day, end_day = days[0].strip(), days[1].strip()
                    if start_day not in self.days_map or end_day not in self.days_map:
                        raise ValueError(f"Invalid day name. Valid days are: {', '.join(self.days_map.keys())}")
                    current_day = start_day
                    while True:
                        operating_hours[current_day] = (start_dt, end_dt)
                        if current_day == end_day:
                            break
                        current_day = list(self.days_map.keys())[
                            (self.days_map[current_day] + 1) % 7
                        ]
                else:
                    day = days[0].strip()
                    if day not in self.days_map:
                        raise ValueError(f"Invalid day name '{day}'. Valid days are: {', '.join(self.days_map.keys())}")
                    operating_hours[day] = (start_dt, end_dt)
                
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in line '{line}': {str(e)}")
        
        if not operating_hours:
            raise ValueError("No valid operating hours found")
        
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
    if len(sys.argv) != 3:
        print("Usage: python -m src.main <movies_file> <hours_file>")
        sys.exit(1)

    movies_file = sys.argv[1]
    hours_file = sys.argv[2]

    try:
        # Initialize calculator
        calculator = TheaterShowtimes()
        
        # Read and parse input files
        with open(movies_file, 'r') as f:
            movies_data = f.read()
            
        with open(hours_file, 'r') as f:
            hours_data = f.read()
            
        # Parse the data
        movies = []
        for line in movies_data.strip().split('\n')[1:]:  # Skip header
            title, year, rating, runtime = line.strip().split(',')
            movies.append({
                'Movie Title': title,
                'Release Year': year,
                'MPAA Rating': rating,
                'Run Time': runtime
            })
            
        operating_hours = calculator.parse_operating_hours(hours_data)
        
        # Calculate showtimes for each day
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        all_showtimes = {}
        
        for day in days:
            try:
                day_showtimes = calculator.calculate_showtimes(movies, operating_hours, day)
                if day_showtimes:
                    all_showtimes[day] = day_showtimes
            except KeyError:
                continue  # Skip days without operating hours
        
        # Display results
        print("\nTheater Showtimes:")
        print("=================")
        
        for day, showtimes in all_showtimes.items():
            print(f"\n{day}:")
            for show in showtimes:
                print(f"  {show['movie']}: {show['start_time']} - {show['end_time']}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data format - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
