#!/usr/bin/env python3
"""
Mapper for Average MidtermScore per course.

Input : CSV line from Enrollment.csv
Output: course_id<TAB>midterm_score,1
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
        midterm = parsed.get("midterm_score")

        if course_id is None or midterm is None:
            continue

        sys.stdout.write(f"{course_id}\t{midterm},1\n")


if __name__ == "__main__":
    main()

