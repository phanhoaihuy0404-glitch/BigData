#!/usr/bin/env python3
"""
Reducer for computing average score per course.

Input : CourseID<TAB>TotalScore   (from mapper output, sorted by CourseID)
Output: CourseID<TAB>AverageScore
"""

import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():
    current_course = None
    sum_scores = 0.0
    count = 0

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

        if score < 0 or score > 10:
            continue
    

        if current_course is None:
            current_course = course_id
            sum_scores = score
            count = 1
            
        elif course_id == current_course:
            sum_scores += score
            count += 1

        else:
            # Emit average for previous course
            avg = round(sum_scores / count, 2)
            emit(current_course, avg)
            current_course = course_id
            sum_scores = score
            count = 1


    # Emit last course
    if current_course is not None and count > 0:
        avg = round(sum_scores / count, 2)
        emit(current_course, avg)


if __name__ == "__main__":
    main()

