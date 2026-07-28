

import sys
import os

# Ensure project root is in path so 'parser_1' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from parser_1.csv_parser import parse_enrollment


def main():
    
    # Skip header line
    first_line = sys.stdin.readline()
    # Process the rest
    for line in sys.stdin:
        parsed = parse_enrollment(line)
        if not parsed:
            continue

        course_id = parsed.get("course_id")
        student_id = parsed.get("student_id")
        total_score = parsed.get("total_score")

        if course_id is None or student_id is None or total_score is None:
            continue

        sys.stdout.write(f"{course_id}\t{student_id}\t{total_score}\n")


if __name__ == "__main__":
    main()

