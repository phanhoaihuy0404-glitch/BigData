#!/usr/bin/env python3
"""
Mapper for counting students per course (CourseID).

Input : CSV line from Enrollment.csv (header skipped automatically)
Output: CourseID<TAB>1   (one record per enrollment)
"""

import sys
import os

# Ensure project root is in path so 'parser' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

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
        course_id = record["course_id"]
        emit(course_id, 1)


if __name__ == "__main__":
    main()

