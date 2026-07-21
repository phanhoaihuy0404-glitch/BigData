#!/usr/bin/env python3
"""
Reducer for computing grade distribution per course.

Input : CourseID,LetterGrade<TAB>1   (from mapper output, sorted by key)
Output: CourseID<TAB>LetterGrade<TAB>Count
"""

import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    current_key = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        key, value_str = parts
        try:
            value = int(value_str)
        except ValueError:
            continue

        if current_key is None:
            current_key = key
            current_count = value
        elif key == current_key:
            current_count += value
        else:
            # Emit: CourseID,LetterGrade -> count
            emit(current_key, current_count)
            current_key = key
            current_count = value

    if current_key is not None:
        emit(current_key, current_count)


if __name__ == "__main__":
    main()

