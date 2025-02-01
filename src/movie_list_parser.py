"""Parses a CSV file containing a list of movies and returns a list of Movie objects."""
import csv
from datetime import datetime, time
from typing import List
from .movie import Movie

def parse_runtime(runtime_str: str) -> datetime.time:
    """
    Parse runtime string into time object, handling various formats.
    
    Args:
        runtime_str: String in format "H:MM" or "HH:MM"
        
    Returns:
        time object
        
    Raises:
        ValueError: If runtime format is invalid
    """
    try:
        # Handle single-digit hours
        parts = runtime_str.split(':')
        if len(parts) != 2:
            raise ValueError("Invalid runtime format")
            
        hours = int(parts[0])
        minutes = int(parts[1])
        
        # Validate hours and minutes
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError("Invalid runtime format")
            
        return time(hour=hours, minute=minutes)
    except (ValueError, IndexError):
        raise ValueError("Invalid runtime format")

def parse_movie_list(filename: str) -> List[Movie]:
    """
    Parse the movie list CSV file and return a list of Movie objects.
    
    Args:
        filename: Path to the movies CSV file
        
    Returns:
        List of Movie objects
        
    Raises:
        ValueError: If the file format is invalid or file not found
    """
    movies: List[Movie] = []
    expected_headers = ["Movie Title", "Release Year", "MPAA Rating", "Run Time"]
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Check if file is empty
            first_line = file.readline().strip()
            if not first_line:
                raise ValueError("Invalid movie data format")
                
            # Validate headers
            headers = [h.strip() for h in first_line.split(',')]
            if headers != expected_headers:
                raise ValueError("Invalid movie data format")
                
            # Parse movies
            for line in file:
                if not line.strip():
                    continue
                    
                try:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) != 4:
                        raise ValueError("Invalid movie data format")
                        
                    title, year_str, rating, runtime_str = parts
                    
                    try:
                        year = int(year_str)
                    except ValueError:
                        raise ValueError("Invalid year format")
                        
                    try:
                        run_time = parse_runtime(runtime_str)
                    except ValueError:
                        raise ValueError("Invalid runtime format")
                    
                    movies.append(Movie(title, year, rating, run_time))
                except ValueError as e:
                    raise ValueError(str(e))
                    
        return movies
    except FileNotFoundError as e:
        raise ValueError(f"File not found: {filename}") from e
