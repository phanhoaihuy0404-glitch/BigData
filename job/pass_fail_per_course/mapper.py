import sys

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

        try:
            total_score = float(total_score)
        except ValueError:
            continue

        if total_score >= 5:
            emit(course_id, "PASS")
        else:
            emit(course_id, "FAIL")


if __name__ == "__main__":
    main()