#!/usr/bin/env python3
"""mapper/avg_midterm_per_course.py

Hadoop Streaming - Average MidtermScore per course

Mapper rules:
- Read Enrollment rows from sys.stdin
- Use EnrollmentParser.parse(line)
- Emit: course_id\t{midterm_score},1

Output format:
  course_id\tmidterm_score,1
"""

import sys

try:
    from parser.enrollment_parser import EnrollmentParser
except ImportError:
    from parser.enrollment_parser import EnrollmentParser  # type: ignore


def main():
    for line in sys.stdin:
        parsed = EnrollmentParser.parse(line)
        if not parsed:
            continue

        course_id = parsed.get("course_id")
        midterm = parsed.get("midterm_score")

        if course_id is None or midterm is None:
            continue

        # midterm is expected to be float from parser
        sys.stdout.write(f"{course_id}\t{midterm},1\n")


if __name__ == "__main__":
    main()

