#!/usr/bin/env python3
"""Main module for the theater showtimes program."""
import sys
import os
from .movie_list_parser import parse_movie_list
from .hours_parser import parse_hours_file
from .calculate_showtimes import calculate_showtimes
from .display_showtimes import display_showtimes

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
