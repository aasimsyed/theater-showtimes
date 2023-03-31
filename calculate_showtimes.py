from utilities import time_to_minutes, minutes_to_time

def calculate_showtimes(movies, hours):
    showtimes = {}

    for movie in movies:
        # Format the runtime string in minutes
        runtime_minutes = time_to_minutes(movie.run_time)
        runtime_formatted = minutes_to_time(runtime_minutes)

        # Create a display title that includes the movie title, MPAA rating, and runtime
        display_title = f"{movie.title} - Rated {movie.mpaa_rating}, {runtime_formatted}"

        for day, (opening_time, closing_time) in hours.items():
            # Calculate the ready time after theater set up for each day
            open_ready_minutes = time_to_minutes(opening_time) + 60

            # Get the closing time for each day in minutes
            closing_time_minutes = time_to_minutes(closing_time)

            # Calculate the start time for the last movie of the day
            last_movie_start_time = closing_time_minutes - runtime_minutes

            # Round back to the nearest 5 minute interval
            rounded_last_movie_start_time = last_movie_start_time - (last_movie_start_time % 5)

            # 35 minutes to clean the theater before next movie
            last_end_minutes = rounded_last_movie_start_time - 35  

            # Add the last movie start time to the list of showtimes for this movie and day
            if day not in showtimes:
                showtimes[day] = {}
            
            # Check if movie title key exists in day dict
            if display_title not in showtimes[day]:
                showtimes[day][display_title] = []

            showtimes[day][display_title].append((minutes_to_time(rounded_last_movie_start_time), minutes_to_time(rounded_last_movie_start_time + runtime_minutes)))

            # Calculate the start time for all other shows
            current_end_time_minutes = last_end_minutes

            while current_end_time_minutes - runtime_minutes >= open_ready_minutes:
                start_minutes = current_end_time_minutes - runtime_minutes
                start_minutes -= (start_minutes % 5)
                end_minutes = current_end_time_minutes
                show_start = minutes_to_time(start_minutes)
                show_end = minutes_to_time(end_minutes)

                # Add the showtime to the list of showtimes for this movie and day
                showtimes[day][display_title].append((show_start, show_end))

                # Move back to the previous showtime and account for cleaning time
                current_end_time_minutes -= (runtime_minutes + 35)
                current_end_time_minutes -= (current_end_time_minutes % 5)

    # Sort showtimes by start time for each day
    for day in showtimes:
        for title in showtimes[day]:
            showtimes[day][title].sort()

    return showtimes
