#!/usr/bin/env python3
"""This is the main module for the theater showtimes program."""
import sys
import os
from utilities import is_valid_csv
from movie_list_parser import parse_movie_list
from hours_parser import parse_hours_file
from calculate_showtimes import calculate_showtimes
from display_showtimes import display_showtimes

def main():
    """The main function for the theater showtimes program."""
    if len(sys.argv) != 2:
        print("Usage: ./theater_showtimes.py <movie_list_file>")
        sys.exit(1)

    # Get the path to the hours.txt file
    hours_file = os.path.join(os.path.dirname(__file__), "..", "resources", "hours.txt")
    hours = parse_hours_file(hours_file)

    # Get the path to the movie list file
    movie_list_file = sys.argv[1]

    # Validate the movie list file
    try:
        is_valid_csv(movie_list_file)
    except ValueError as error:
        print(error)
        sys.exit(1)

    # Parse the movie list file
    movies = parse_movie_list(movie_list_file)

    # Calculate the showtimes
    showtimes = calculate_showtimes(movies, hours)

    # Display the showtimes
    display_showtimes(showtimes)

if __name__ == "__main__":
    main()
