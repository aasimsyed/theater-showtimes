#!/usr/bin/env python3
import sys
from utilities import is_valid_csv
from movie_list_parser import parse_movie_list
from hours_parser import parse_hours_file
from calculate_showtimes import calculate_showtimes
from display_showtimes import display_showtimes

def main():
    if len(sys.argv) != 2:
        print("Usage: ./theater_showtimes.py <movie_list_file>")
        sys.exit(1)

    hours_file = "hours.txt"
    hours = parse_hours_file(hours_file)

    movie_list_file = sys.argv[1]
    if not is_valid_csv(movie_list_file):
        print(f"{movie_list_file} is not a valid CSV file.")
        sys.exit(1)

    movies = parse_movie_list(movie_list_file)

    showtimes = calculate_showtimes(movies, hours)
    display_showtimes(showtimes)

if __name__ == "__main__":
    main()
