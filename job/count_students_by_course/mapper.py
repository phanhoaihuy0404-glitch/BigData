import sys
import os

from csv_parser import parse_enrollment


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
        course_id = record["CourseID"]
        emit(course_id, 1)


if __name__ == "__main__":
    main()

