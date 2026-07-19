#!/usr/bin/env python3
"""mapper/lowest_score_per_course.py

Hadoop Streaming - Lowest score of each course

Mapper:
- Read Enrollment rows from sys.stdin
- Use EnrollmentParser.parse(line)
- Emit: course_id\ttotal_score
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
        total_score = parsed.get("total_score")
        if course_id is None or total_score is None:
            continue

        sys.stdout.write(f"{course_id}\t{total_score}\n")


if __name__ == "__main__":
    main()

