class Movie:
    def __init__(self, title, release_year, mpaa_rating, run_time):
        self.title = title
        self.release_year = release_year
        self.mpaa_rating = mpaa_rating
        self.run_time = run_time

    def __str__(self):
        run_time_str = f"{self.run_time.hour}:{self.run_time.minute:02d}"
        return f"{self.title} - Rated {self.mpaa_rating}, {run_time_str}"
