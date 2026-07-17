import sys

from parser.enrollment_parser import EnrollmentParser


def emit(key, value):
    print(f"{key}\t{value}")


def main():

    for line in sys.stdin:

        record = EnrollmentParser.parse(line)

        if record is None:
            continue

        course_id = record["course_id"]

        emit(course_id, 1)


if __name__ == "__main__":
    main()