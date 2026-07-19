#!/usr/bin/env python3
"""reducer/avg_midterm_per_course.py

Hadoop Streaming - Average MidtermScore per course

Input format (key\tvalue) from mapper:
  course_id\tmidterm_score,1

Reducer:
- For each course_id, sum midterm_score and counts
- Compute average with proper float conversion
- Print: course_id\tAVG (2 decimal places)

Notes:
- Handle malformed values via try/except
- Optimized streaming reducer: assumes input is sorted by key
"""

import sys


def emit(course_id: str, avg: float) -> None:
    sys.stdout.write(f"{course_id}\t{avg:.2f}\n")


def main():
    current_course = None
    sum_scores = 0.0
    count = 0

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            course_id, payload = raw.split("\t", 1)
        except ValueError:
            continue

        # payload format: "score,count"
        try:
            score_str, cnt_str = payload.split(",", 1)
        except ValueError:
            continue

        try:
            score = float(score_str)
            cnt = int(cnt_str)
        except (ValueError, TypeError):
            # skip invalid records
            continue

        if current_course is None:
            current_course = course_id

        if course_id != current_course:
            if count > 0:
                avg = sum_scores / count
            else:
                avg = 0.0
            emit(current_course, avg)

            current_course = course_id
            sum_scores = 0.0
            count = 0

        sum_scores += score * cnt  # cnt is expected to be 1
        count += cnt

    # flush last key
    if current_course is not None:
        avg = (sum_scores / count) if count > 0 else 0.0
        emit(current_course, avg)


if __name__ == "__main__":
    main()

