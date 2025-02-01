"""Unit tests for theater showtimes application."""
from datetime import time, datetime, timedelta
import pytest
from src.movie import Movie
from src.hours_parser import parse_hours_file, TimeRange, parse_time_range
from src.movie_list_parser import parse_movie_list
from src.calculate_showtimes import (
    calculate_showtimes,
    add_minutes_to_time,
    time_diff_minutes
)
from src.utilities import str_to_time, minutes_to_time
from src.theater_showtimes import TheaterShowtimes

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

# Move shared fixtures to module level
@pytest.fixture
def calculator():
    return TheaterShowtimes()

@pytest.fixture
def operating_hours():
    return {
        'Monday': (datetime.strptime('9:00AM', '%I:%M%p'),
                  datetime.strptime('11:30PM', '%I:%M%p')),
        'Saturday': (datetime.strptime('12:00PM', '%I:%M%p'),
                    datetime.strptime('11:59PM', '%I:%M%p'))
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
        assert hours["Monday"] == parse_time_range("12:00am-11:59pm")

    def test_parse_invalid_day_name(self, tmp_path):
        """Test handling invalid day names."""
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text("InvalidDay 8:00am - 11:00pm")
        with pytest.raises(ValueError, match="No valid hours found in file"):
            parse_hours_file(str(hours_file))

    def test_parse_overlapping_ranges(self, tmp_path):
        """Test handling overlapping day ranges."""
        hours_file = tmp_path / "hours.txt"
        hours_file.write_text(
            "Monday - Wednesday 8:00am - 5:00pm\n"
            "Wednesday - Friday 6:00pm - 11:00pm"
        )
        hours = parse_hours_file(str(hours_file))
        assert hours["Wednesday"] == parse_time_range("6:00pm-11:00pm")

# Showtime Calculation Tests (Enhanced)
class TestShowtimeCalculation:
    """Tests for showtime calculation functionality."""

    @pytest.fixture
    def sample_movies(self):
        return [
            {'Movie Title': 'Short Movie', 'Run Time': '1:30'},
            {'Movie Title': 'Medium Movie', 'Run Time': '2:00'},
            {'Movie Title': 'Long Movie', 'Run Time': '2:45'}
        ]

    def test_calculate_showtimes_multiple_short_movies(self, calculator, sample_movies, operating_hours):
        showtimes = calculator.calculate_showtimes(
            [sample_movies[0]], operating_hours, 'Monday')
        assert len(showtimes) > 0
        assert showtimes[0]['movie'] == 'Short Movie'

    def test_calculate_showtimes_boundary_conditions(self, calculator, operating_hours):
        movies = [{'Movie Title': 'Test Movie', 'Run Time': '2:00'}]
        showtimes = calculator.calculate_showtimes(movies, operating_hours, 'Monday')
        assert len(showtimes) > 0
        first_show = datetime.strptime(showtimes[0]['start_time'], '%I:%M %p')
        assert first_show >= operating_hours['Monday'][0]

    def test_calculate_showtimes_exact_fit(self, calculator, operating_hours):
        movies = [{'Movie Title': 'Exact Fit', 'Run Time': '2:00'}]
        showtimes = calculator.calculate_showtimes(movies, operating_hours, 'Monday')
        assert len(showtimes) > 0
        last_show = datetime.strptime(showtimes[-1]['end_time'], '%I:%M %p')
        assert last_show <= operating_hours['Monday'][1]

# Integration Tests (Enhanced)
class TestIntegration:
    """Integration tests for the entire workflow."""
    
    def test_full_integration_edge_cases(self, calculator, operating_hours):
        """Test full day scheduling with multiple movies"""
        movies = [
            {'Movie Title': 'Early Show', 'Run Time': '1:30'},  # 90 min + 30 cleanup = 2h
            {'Movie Title': 'Late Show', 'Run Time': '2:00'}    # 120 min + 30 cleanup = 2.5h
        ]
        
        # Monday hours are 9:00 AM to 11:30 PM (14.5 hours)
        showtimes = calculator.calculate_showtimes(movies, operating_hours, 'Monday')
        
        # Calculate minimum expected shows:
        # - Operating hours: 14.5 hours (870 minutes)
        # - Early Show total time: 120 minutes
        # - Late Show total time: 150 minutes
        # We should fit at least 5 shows (3 short + 2 long) in a day
        assert len(showtimes) >= 5
        
        # Verify show times are properly spaced
        for i in range(len(showtimes) - 1):
            current_end = datetime.strptime(showtimes[i]['end_time'], '%I:%M %p')
            next_start = datetime.strptime(showtimes[i + 1]['start_time'], '%I:%M %p')
            # Verify cleanup time is respected
            cleanup_time = (next_start - current_end).total_seconds() / 60
            assert cleanup_time >= 30 