#!/usr/bin/env python3
"""
Reducer for finding the highest score per course.

Input : CourseID<TAB>TotalScore   (from mapper output, sorted by CourseID)
Output: CourseID<TAB>HighestScore
"""

import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    current_course = None
    max_score = float("-inf")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        course_id, score_str = parts
        try:
            score = float(score_str)
        except ValueError:
            continue

        if current_course is None:
            current_course = course_id
            max_score = score
        elif course_id == current_course:
            if score > max_score:
                max_score = score
        else:
            emit(current_course, max_score)
            current_course = course_id
            max_score = score

    if current_course is not None and max_score != float("-inf"):
        emit(current_course, max_score)


if __name__ == "__main__":
    main()

