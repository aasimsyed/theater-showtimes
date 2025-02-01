"""Movie class for theater showtimes."""
from datetime import time
from dataclasses import dataclass

@dataclass
class Movie:
    """
    Represents a movie with its details.
    
    Attributes:
        title: Movie title
        release_year: Year the movie was released
        mpaa_rating: MPAA rating (e.g., 'PG-13', 'R')
        run_time: Movie duration as time object
    """
    title: str
    release_year: int
    mpaa_rating: str
    run_time: time

    def __str__(self) -> str:
        """Return a string representation of the movie."""
        run_time_str = f"{self.run_time.hour}:{self.run_time.minute:02d}"
        return f"{self.title} - Rated {self.mpaa_rating}, {run_time_str}"
