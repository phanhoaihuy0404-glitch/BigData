#!/usr/bin/env python3
"""reducer/pass_fail_per_course.py

Hadoop Streaming - Pass / Fail statistics per course

Input:
  course_id\tPass
  course_id\tFail

Reducer output:
When course_id changes, print:
  course_id\tPass:{pass_count},Fail:{fail_count}

Optimized reducer:
- Assumes input is sorted by key (course_id)
- Streams aggregation with current_course
"""

import sys


def main():
    current_course = None
    pass_count = 0
    fail_count = 0

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            course_id, label = raw.split("\t", 1)
        except ValueError:
            continue

        label = label.strip()
        if current_course is None:
            current_course = course_id

        if course_id != current_course:
            sys.stdout.write(
                f"{current_course}\tPass:{pass_count},Fail:{fail_count}\n"
            )
            current_course = course_id
            pass_count = 0
            fail_count = 0

        # Count pass/fail
        if label == "Pass":
            pass_count += 1
        elif label == "Fail":
            fail_count += 1
        # else: ignore malformed

    if current_course is not None:
        sys.stdout.write(
            f"{current_course}\tPass:{pass_count},Fail:{fail_count}\n"
        )


if __name__ == "__main__":
    main()

