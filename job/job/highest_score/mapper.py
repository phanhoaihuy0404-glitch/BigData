import sys
import os

# Ensure project root is in path so 'parser_1' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from parser_1.csv_parser import parse_enrollment


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    # Skip header line
    first_line = sys.stdin.readline()
    # Process the rest
    for line in sys.stdin:
        record = parse_enrollment(line)
        if record is None:
            continue
        key = record["course_id"]
        value = record["total_score"]
        emit(key, value)


if __name__ == "__main__":
    main()

