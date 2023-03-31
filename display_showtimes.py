import calendar
from datetime import datetime, timedelta
from utilities import minutes_to_time, time_to_minutes, weekdays

def display_showtimes(showtimes):
    # Print each day's showtimes
    for day, movies in showtimes.items():
        # Calculate the date for the next available day with respect to today
        
        # Get the current day of the week
        today = datetime.today().weekday()
        
        # Get the index of a day of the week
        today_index = (today) % 7
        day_index = weekdays.index(day.lower())

        # Calculate the number of days until the next day of the week
        days_since_today = (day_index - today_index) % 7
        next_available_day = datetime.today() + timedelta(days=days_since_today)

        # Print the day and date
        print(f"{day} {next_available_day.month}/{next_available_day.day}/{next_available_day.year}\n")

        # Print each movie's showtimes
        for title in movies:
            # Print the movie title and runtime
            print(f"{title}")

            # Print each showtime for this movie on this day
            for show_start, show_end in movies[title]:
                print(f"  {show_start} - {show_end}")

            print()  # Print a blank line between movies
