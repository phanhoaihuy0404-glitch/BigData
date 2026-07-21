#!/usr/bin/env python3
"""
Mapper for Course performance analytics (multi-metrics).

Input : CSV line from Enrollment.csv
Output: course_id<TAB>total_score,1,<is_pass>,letter_grade
"""

import sys
import os

# Ensure project root is in path so 'parser' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from parser.enrollment_parser import EnrollmentParser


def main():
    # Skip header line
    first_line = sys.stdin.readline()
    # Process the rest
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

        sys.stdout.write(
            f"{course_id}\t{total_score},1,{is_pass},{letter_grade}\n"
        )


if __name__ == "__main__":
    main()

