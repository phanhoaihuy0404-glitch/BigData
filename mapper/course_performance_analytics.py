#!/usr/bin/env python3
"""mapper/course_performance_analytics.py

Hadoop Streaming - Course performance analytics (multi-metrics)

Mapper output (composite value):
  course_id\ttotal_score,1,<is_pass>,letter_grade

Where:
- is_pass = 1 if total_score >= 4.0 else 0
- letter_grade is the raw letter (e.g., A, B, C...)

Rules:
- Read Enrollment rows from sys.stdin
- Use EnrollmentParser.parse(line)
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
        letter_grade = parsed.get("letter_grade")

        if course_id is None or total_score is None or letter_grade is None:
            continue

        is_pass = 1 if total_score >= 4.0 else 0

        # composite payload
        # total_score,1,pass_flag,letter_grade
        sys.stdout.write(
            f"{course_id}\t{total_score},1,{is_pass},{letter_grade}\n"
        )


if __name__ == "__main__":
    main()

