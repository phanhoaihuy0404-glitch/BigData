#!/usr/bin/env python3
"""
Reducer for counting enrollments per course (used for Top N analysis).

Input : CourseID<TAB>1   (from mapper output, sorted by CourseID)
Output: CourseID<TAB>EnrollmentCount
"""

import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    current_course = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        course_id, value_str = parts
        try:
            value = int(value_str)
        except ValueError:
            continue

        if current_course is None:
            current_course = course_id
            current_count = value
        elif course_id == current_course:
            current_count += value
        else:
            emit(current_course, current_count)
            current_course = course_id
            current_count = value

    if current_course is not None:
        emit(current_course, current_count)


if __name__ == "__main__":
    main()

