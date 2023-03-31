import csv
from datetime import datetime
from movie import Movie

def parse_movie_list(file_path):
    movies = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        for row in reader:
            title = row["Movie Title"].strip()
            release_year = int(row["Release Year"].strip())
            mpaa_rating = row["MPAA Rating"].strip()
            run_time = datetime.strptime(row["Run Time"].strip(), "%I:%M")
            movies.append(Movie(title, release_year, mpaa_rating, run_time))
    return movies
