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
        total_score = record["TotalScore"]

        emit(course_id, total_score)


if __name__ == "__main__":
    main()