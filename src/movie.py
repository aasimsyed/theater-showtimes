from dataclasses import dataclass
from datetime import time

@dataclass
class Movie:
    title: str
    release_year: int
    mpaa_rating: str
    run_time: time

    def __str__(self) -> str:
        run_time_str = f"{self.run_time.hour}:{self.run_time.minute:02d}"
        return f"{self.title} - Rated {self.mpaa_rating}, {run_time_str}"
