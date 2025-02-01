#!/usr/bin/env python3
"""Main entry point for theater showtimes calculator."""
import sys
from .theater_showtimes import main

def run():
    """Main entry point for the program."""
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run() 