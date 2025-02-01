# Theater Showtimes Calculator

Calculate optimal movie showtimes for a theater based on operating hours.

## Features

- Parse movie lists with titles, ratings, and runtimes
- Handle theater operating hours by day of week
- Calculate optimal showtimes with cleanup periods
- Support multiple movies per day
- Validate time formats and ranges

## Installation

1. Clone the repository:

```bash
git clone https://github.com/username/theater-showtimes.git
cd theater-showtimes
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Create a movies CSV file:

```csv
Movie Title,Release Year,MPAA Rating,Run Time
Test Movie,2023,PG-13,2:00
```

2. Create a theater hours text file:

```text
Monday - Friday 9:00am - 11:30pm
Saturday - Sunday 12:00pm - 11:59pm
```

3. Run the calculator:

```bash
python -m src.main movies.csv hours.txt
```

## Testing

Run tests with pytest:

```bash
python -m pytest
```

## License

[MIT][license]

[license]: ./LICENSE
