#!/usr/bin/env python3
"""
Reducer for finding the highest score per course.

Input : course_id<TAB>student_id<TAB>total_score   (from mapper, sorted by course_id)
Output: course_id<TAB>student_id<TAB>max_score
"""

import sys


def main():
    current_course = None
    current_student = None
    max_score = float('-inf')

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        #Check
        try:
            course_id, student_id, score_str = raw.split("\t", 2)
        except ValueError:
            continue

        try:
            score = float(score_str)
        except (ValueError, TypeError):
            continue

        if current_course is None:
            current_course = course_id
            current_student = student_id
            max_score = score

        if course_id != current_course:
            sys.stdout.write(f"{current_course}\t{current_student}\t{max_score}\n")
            current_course = course_id
            current_student = student_id
            max_score = score
        else:
            if score > max_score:
                max_score = score
                current_student = student_id

    if current_course is not None:
        sys.stdout.write(f"{current_course}\t{current_student}\t{max_score}\n")


if __name__ == "__main__":
    main()

