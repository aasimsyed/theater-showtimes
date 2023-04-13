"""Test cases for the calculate_showtimes function."""
from movie import Movie
from calculate_showtimes import calculate_showtimes
from utilities import str_to_time as st
from utilities import parse_run_time as prt

def test_single_movie_single_day():
    """Test case for a single movie and single day with valid showtimes."""

    # Prepare the movie data
    movie_data = [
        Movie(
            title="There's Something About Mary",
            release_year=1998,
            mpaa_rating="R",
            run_time=prt("2:14")
        )
    ]

    # Prepare the theater hours
    theater_hours = {
        "Monday": (st("8:00am"), st("11:00pm"))
    }

    # Call the calculate_showtimes function with the test data
    calculated_showtimes = calculate_showtimes(movie_data, theater_hours)

    # Define the expected showtimes
    expected_showtimes = {
        "Monday": {
            "There's Something About Mary - Rated R, 2:14": [
                ('9:25', '11:39'),
                ("12:15", "14:29"),
                ("15:05", "17:19"),
                ("17:55", "20:09"),
                ("20:45", "22:59")
            ]
        }
    }

    # Assert that the calculated showtimes match the expected showtimes
    assert calculated_showtimes == expected_showtimes, (
    f"Expected {expected_showtimes}, but got {calculated_showtimes}"
)

def test_single_movie_no_showtimes():
    """Test case for a single movie and single day with no valid showtimes"""
    # Test case for a single movie and single day with no valid showtimes
    # Prepare the movie data
    movie_data = [
        Movie(
            title="There's Something About Mary",
            release_year=1998,
            mpaa_rating="R",
            run_time=prt("2:14")
        )
    ]

    # Prepare the theater hours
    theater_hours = {
        "Monday": (st("8:00am"), st("10:00am"))
    }

    # Call the calculate_showtimes function with the test data
    calculated_showtimes = calculate_showtimes(movie_data, theater_hours)

    # Define the expected showtimes (empty list)
    expected_showtimes = {}

    # Assert that the calculated showtimes match the expected showtimes
    assert calculated_showtimes == expected_showtimes, (
        f"Expected {expected_showtimes}, but got {calculated_showtimes}"
    )

def test_empty_movies_list():
    """Test case for an empty movies list"""
    # Prepare the movie data (empty list)
    movie_data = []

    # Prepare the theater hours
    theater_hours = {
        "Monday": (st("8:00am"), st("11:00pm"))
    }

    # Call the calculate_showtimes function with the test data
    calculated_showtimes = calculate_showtimes(movie_data, theater_hours)

    # Define the expected showtimes (empty dictionary)
    expected_showtimes = {}

    # Assert that the calculated showtimes match the expected showtimes
    assert calculated_showtimes == expected_showtimes, (
        f"Expected {expected_showtimes}, but got {calculated_showtimes}"
    )


def test_empty_hours_dict():
    """Test case for an empty hours dictionary"""
    # Test case for an empty hours dictionary
    # Prepare the movie data
    movie_data = [
        Movie(
            title="There's Something About Mary",
            release_year=1998,
            mpaa_rating="R",
            run_time=prt("2:14")
        )
    ]

    # Prepare the theater hours
    theater_hours = {}

    # Call the calculate_showtimes function with the test data
    calculated_showtimes = calculate_showtimes(movie_data, theater_hours)

    # Define the expected showtimes (empty list)
    expected_showtimes = {}

    # Assert that the calculated showtimes match the expected showtimes
    assert calculated_showtimes == expected_showtimes, (
        f"Expected {expected_showtimes}, but got {calculated_showtimes}"
    )


def run_tests():
    """Run all of the test cases."""
    print("Running tests...")
    test_single_movie_single_day()
    test_single_movie_no_showtimes()
    test_empty_movies_list()
    test_empty_hours_dict()
    print("All tests passed.")


if __name__ == '__main__':
    run_tests()
