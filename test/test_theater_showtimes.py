"""Unit tests for theater showtimes application."""
from datetime import time
import pytest
from src.movie import Movie
from src.hours_parser import parse_hours_file, TimeRange
from src.movie_list_parser import parse_movie_list
from src.calculate_showtimes import (
    calculate_showtimes,
    add_minutes_to_time,
    time_diff_minutes
)
from src.utilities import str_to_time, minutes_to_time

# Test Data Fixtures
@pytest.fixture
def sample_movie():
    """Return a sample movie for testing."""
    return Movie(
        title="Test Movie",
        release_year=2023,
        mpaa_rating="PG-13",
        run_time=time(2, 0)  # 2 hours
    )

@pytest.fixture
def sample_hours():
    """Return sample theater hours for testing."""
    return {
        "Monday": TimeRange(time(8, 0), time(23, 0)),
        "Tuesday": TimeRange(time(8, 0), time(23, 0)),
        "Wednesday": TimeRange(time(8, 0), time(23, 0)),
        "Thursday": TimeRange(time(8, 0), time(23, 30)),
        "Friday": TimeRange(time(10, 30), time(23, 30)),
        "Saturday": TimeRange(time(10, 30), time(23, 30)),
        "Sunday": TimeRange(time(10, 30), time(23, 30))
    }

# Utility Function Tests
class TestUtilities:
    """Tests for utility functions."""
    
    @pytest.mark.parametrize("time_str,expected", [
        ("8:00am", time(8, 0)),
        ("11:30pm", time(23, 30)),
        ("12:00pm", time(12, 0)),
        ("12:00am", time(0, 0)),
    ])
    def test_str_to_time_valid(self, time_str, expected):
        """Test valid time string parsing."""
        assert str_to_time(time_str) == expected

    @pytest.mark.parametrize("time_str", [
        "25:00am",  # Invalid hour
        "8:60am",   # Invalid minute
        "8:00",     # Missing meridian
        "8am",      # Missing minutes
        "",         # Empty string
    ])
    def test_str_to_time_invalid(self, time_str):
        """Test invalid time string handling."""
        with pytest.raises(ValueError):
            str_to_time(time_str)

    @pytest.mark.parametrize("minutes,expected", [
        (0, time(0, 0)),
        (60, time(1, 0)),
        (90, time(1, 30)),
        (1440, time(0, 0)),  # Full day wraps around
    ])
    def test_minutes_to_time(self, minutes, expected):
        """Test converting minutes to time."""
        assert minutes_to_time(minutes) == expected

# Time Manipulation Tests
class TestTimeManipulation:
    """Tests for time manipulation functions."""
    
    @pytest.mark.parametrize("base_time,minutes,expected", [
        (time(8, 0), 30, time(8, 30)),
        (time(8, 0), 60, time(9, 0)),
        (time(23, 30), 30, time(0, 0)),
        (time(23, 0), 120, time(1, 0)),
    ])
    def test_add_minutes_to_time(self, base_time, minutes, expected):
        """Test adding minutes to time."""
        assert add_minutes_to_time(base_time, minutes) == expected

    @pytest.mark.parametrize("time1,time2,expected", [
        (time(8, 0), time(9, 0), 60),
        (time(8, 0), time(8, 30), 30),
        (time(23, 0), time(1, 0), 120),
        (time(0, 0), time(0, 0), 0),
    ])
    def test_time_diff_minutes(self, time1, time2, expected):
        """Test calculating time differences."""
        assert time_diff_minutes(time1, time2) == expected

# Movie List Parser Tests (Enhanced)
class TestMovieListParser:
    """Tests for movie list parsing functionality."""
    
    def test_parse_valid_movie_list_multiple(self, tmp_path):
        """Test parsing multiple valid movies."""
        movie_file = tmp_path / "movies.txt"
        movie_file.write_text(
            "Movie Title,Release Year,MPAA Rating,Run Time\n"
            "Movie 1,2023,PG-13,2:00\n"
            "Movie 2,2022,R,1:45\n"
            "Movie 3,2024,G,1:30"
        )
        movies = parse_movie_list(str(movie_file))
        assert len(movies) == 3
        assert all(isinstance(m, Movie) for m in movies)

    def test_parse_empty_file(self, tmp_path):
        """Test handling empty file."""
        movie_file = tmp_path / "movies.txt"
        movie_file.write_text("")
        with pytest.raises(ValueError, match="Invalid movie data format"):
            parse_movie_list(str(movie_file))

    def test_parse_missing_header(self, tmp_path):
        """Test handling missing header."""
        movie_file = tmp_path / "movies.txt"
        movie_file.write_text("Test Movie,2023,PG-13,2:00")
        with pytest.raises(ValueError, match="Invalid movie data format"):
            parse_movie_list(str(movie_file))

# Hours Parser Tests (Enhanced)
class TestHoursParser:
    """Tests for theater hours parsing functionality."""
    
    def test_parse_hours_edge_times(self, tmp_path):
        """Test parsing edge case times."""
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text(
            "Monday 12:00am - 11:59pm\n"
            "Tuesday 12:01am - 12:00pm\n"
            "Wednesday 11:59am - 12:01am"
        )
        hours = parse_hours_file(str(hours_file))
        assert len(hours) == 3
        assert hours["Monday"] == TimeRange(time(0, 0), time(23, 59))

    def test_parse_invalid_day_name(self, tmp_path):
        """Test handling invalid day names."""
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text("InvalidDay 8:00am - 11:00pm")
        with pytest.raises(ValueError, match="Invalid hours format"):
            parse_hours_file(str(hours_file))

    def test_parse_overlapping_ranges(self, tmp_path):
        """Test handling overlapping day ranges."""
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text(
            "Monday - Wednesday 8:00am - 5:00pm\n"
            "Wednesday - Friday 6:00pm - 11:00pm"
        )
        hours = parse_hours_file(str(hours_file))
        assert hours["Wednesday"] == TimeRange(time(18, 0), time(23, 0))

# Showtime Calculation Tests (Enhanced)
class TestShowtimeCalculation:
    """Tests for showtime calculation functionality."""
    
    def test_calculate_showtimes_exact_fit(self, theater_hours):
        """Test movie that exactly fits in operating window."""
        movie = Movie("Exact Fit", 2023, "PG", time(14, 30))  # 14.5 hours
        showtimes = calculate_showtimes([movie], theater_hours)
        assert len(showtimes["Monday"][movie.title]) == 1

    def test_calculate_showtimes_multiple_short_movies(self, sample_hours):
        """Test multiple short movies in a day."""
        movies = [
            Movie("Short 1", 2023, "G", time(1, 0)),
            Movie("Short 2", 2023, "G", time(1, 0)),
            Movie("Short 3", 2023, "G", time(1, 0))
        ]
        showtimes = calculate_showtimes(movies, sample_hours)
        day_times = showtimes["Monday"]
        assert all(len(times) > 5 for times in day_times.values())

    def test_calculate_showtimes_boundary_conditions(self, sample_hours):
        """Test boundary conditions for movie times."""
        movie = Movie("Boundary", 2023, "PG", time(2, 0))
        showtimes = calculate_showtimes([movie], sample_hours)
        monday_times = showtimes["Monday"][movie.title]
        
        # First showing should start at opening
        assert monday_times[0] == time(8, 0)
        
        # Last showing should end by closing
        last_end_time = add_minutes_to_time(monday_times[-1], 150)  # 2:30 with cleanup
        assert last_end_time <= time(23, 0)

# Integration Tests (Enhanced)
class TestIntegration:
    """Integration tests for the entire workflow."""
    
    def test_full_integration_edge_cases(self, tmp_path):
        """Test integration with edge cases."""
        movie_file = tmp_path / "movies.txt"
        movie_file.write_text(
            "Movie Title,Release Year,MPAA Rating,Run Time\n"
            "Short Movie,2023,G,0:30\n"
            "Long Movie,2023,PG-13,4:00\n"
            "Edge Movie,2023,R,11:59"
        )
        
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text(
            "Monday - Friday 9:00am - 11:30pm\n"
            "Saturday - Sunday 12:00pm - 11:59pm"
        )
        
        movies = parse_movie_list(str(movie_file))
        hours = parse_hours_file(str(hours_file))
        showtimes = calculate_showtimes(movies, hours)
        
        assert len(movies) == 3
        assert len(hours) == 7
        assert len(showtimes) == 7
        
        # Short movie should have many showings
        assert len(showtimes["Monday"]["Short Movie"]) > 10
        
        # Long movie should have fewer showings
        assert len(showtimes["Monday"]["Long Movie"]) < 5 