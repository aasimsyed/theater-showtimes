"""Displays the showtimes for today's movies."""

from datetime import datetime
from utilities import weekdays

def display_showtimes(showtimes):
    """Displays the showtimes for today's movies."""
    # Get the current day of the week
    today_date = datetime.today()
    today = weekdays[today_date.weekday()].capitalize()

    if today in showtimes:
        # Print the day and date
        date_string = (f"{today_date.month}/"
                        f"{today_date.day}/"
                        f"{today_date.year}")
        print(f"{today} {date_string}\n")

        # Get the movies for today
        movies = showtimes[today]

        # Print each movie's showtimes
        for title in movies:
            # Print the movie title and runtime
            print(f"{title}")

            # Print each showtime for this movie on this day
            for show_start, show_end in movies[title]:
                print(f"  {show_start} - {show_end}")

            print()
    else:
        print(f"No showtimes available for {today}.")
