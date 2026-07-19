#!/usr/bin/env python3
"""reducer/lowest_score_per_course.py

Hadoop Streaming - Lowest score of each course

Input:
  course_id\ttotal_score

Reducer:
- For each course_id, compute minimum total_score
- Assumes input is sorted by key
- Print when course changes:
  course_id\tmin_score
"""

import sys


def main():
    current_course = None
    min_score = float('inf')

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            course_id, score_str = raw.split("\t", 1)
        except ValueError:
            continue

        try:
            score = float(score_str)
        except (ValueError, TypeError):
            continue

        if current_course is None:
            current_course = course_id
            min_score = score

        if course_id != current_course:
            sys.stdout.write(f"{current_course}\t{min_score}\n")
            current_course = course_id
            min_score = score
        else:
            if score < min_score:
                min_score = score

    if current_course is not None:
        sys.stdout.write(f"{current_course}\t{min_score}\n")


if __name__ == "__main__":
    main()

