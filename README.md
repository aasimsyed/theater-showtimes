# Theater Showtimes

Theater Showtimes is a command-line application that helps movie theaters generate showtime schedules for their movies. This application reads movie information from a text file and calculates showtimes based on the theater's hours of operation.

## Configuration

The application requires two text files:

1. **movies.txt**: This file should contain movie information in a comma-separated format. Each line should have the following fields: Movie Title, Release Year, MPAA Rating, and Run Time.

Example:

```csv
Movie Title, Release Year, MPAA Rating, Run Time
There's Something About Mary, 1998, R, 2:14
How to Lose a Guy in 10 Days, 2003, PG-13, 1:56
Knocked Up, 2007, R, 2:08
```

2. **hours.txt**: This file should contain the theater's hours of operation in the following format:

```txt
Monday - Thursday 8:00am - 11:00pm
Friday - Sunday 10:30am - 11:30pm
```

## Usage

To use the application, first, make sure you have Python installed on your system. Then, follow these steps:

1. Clone the repository:

```bash
git clone <https://github.com/your-username/theater-showtimes.git>
```

2. Navigate to the project directory:
```bash
cd theater-showtimes
```

3. Run the application with the movies and hours text files as arguments:
```bash
./theater_showtimes.py movies.txt
```

The application will read the movie and theater hours data from the input files and display the calculated showtimes in the terminal.
