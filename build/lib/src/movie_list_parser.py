"""Parses a CSV file containing a list of movies and returns a list of Movie objects."""""
import csv
from movie import Movie
from utilities import parse_run_time

def parse_movie_list(file_path):
    """Parses a CSV file containing a list of movies and returns a list of Movie objects."""
    movies = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        for row in reader:
            title = row["Movie Title"].strip()
            release_year = int(row["Release Year"].strip())
            mpaa_rating = row["MPAA Rating"].strip()
            run_time = parse_run_time(row["Run Time"].strip())
            movies.append(Movie(title, release_year, mpaa_rating, run_time))
    return movies
