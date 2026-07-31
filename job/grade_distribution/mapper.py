import sys

from csv_parser import parse_enrollment


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    # Skip header
    sys.stdin.readline()

    for line in sys.stdin:

        record = parse_enrollment(line)

        if record is None:
            continue

        letter_grade = record["LetterGrade"].strip().upper()

        if letter_grade == "":
            continue

        emit(letter_grade, 1)


if __name__ == "__main__":
    main()