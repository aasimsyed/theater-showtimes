from utilities import time_to_minutes, minutes_to_time

def calculate_showtimes_for_movie(movie, opening_time, closing_time):
    runtime_minutes = time_to_minutes(movie.run_time)
    display_title = f"{movie.title} - Rated {movie.mpaa_rating}, {minutes_to_time(runtime_minutes)}"
    open_ready_minutes = time_to_minutes(opening_time) + 60
    closing_time_minutes = time_to_minutes(closing_time)

    # Check if the movie's runtime exceeds the available time
    if runtime_minutes > closing_time_minutes - open_ready_minutes:
        return display_title, []

    # Calculate the last showtime that starts before the theater closes
    final_start_minutes = (
        closing_time_minutes
        - runtime_minutes
        - (closing_time_minutes - runtime_minutes) % 5
    )

    showtimes = []
    showtimes.append((
        minutes_to_time(final_start_minutes),
        minutes_to_time(final_start_minutes + runtime_minutes)))

    # Get the previous movie's end time
    previous_end_minutes = final_start_minutes - 36

    while previous_end_minutes - runtime_minutes >= open_ready_minutes:
        start_minutes = previous_end_minutes - runtime_minutes
        start_minutes -= start_minutes % 5
        showtimes.append((
            minutes_to_time(start_minutes),
            minutes_to_time(start_minutes + runtime_minutes)))
        previous_end_minutes -= (runtime_minutes + 36)

    return display_title, showtimes[::-1]

def calculate_showtimes(movies, hours):
    showtimes = {}

    for movie in movies:
        for day, (opening_time, closing_time) in hours.items():
            display_title, day_showtimes = (
                calculate_showtimes_for_movie(movie, opening_time, closing_time)
            )

            if day_showtimes:
                if day not in showtimes:
                    showtimes[day] = {}
                if display_title not in showtimes[day]:
                    showtimes[day][display_title] = []

                showtimes[day][display_title].extend(day_showtimes)

    return showtimes
