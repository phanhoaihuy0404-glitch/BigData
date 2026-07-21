#!/usr/bin/env python3
"""
Mapper for computing average score per course.

Input : CSV line from Enrollment.csv (header skipped automatically)
Output: CourseID<TAB>TotalScore
"""

import sys
import os

# Ensure project root is in path so 'parser' module can be found
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from parser.enrollment_parser import EnrollmentParser


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    # Skip header line
    first_line = sys.stdin.readline()
    # Process the rest
    for line in sys.stdin:
        record = EnrollmentParser.parse(line)
        if record is None:
            continue
        key = record["course_id"]
        value = record["total_score"]
        emit(key, value)


if __name__ == "__main__":
    main()

