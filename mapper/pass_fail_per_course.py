#!/usr/bin/env python3
"""mapper/pass_fail_per_course.py

Hadoop Streaming - Pass / Fail statistics per course

Rules:
- Pass if total_score >= 4.0 else Fail
- Emit: course_id\tPass or course_id\tFail

Mapper rules:
- Read from sys.stdin
- Use EnrollmentParser.parse(line)
"""

import sys

try:
    from parser.enrollment_parser import EnrollmentParser
except ImportError:
    from parser.enrollment_parser import EnrollmentParser  # type: ignore


def main():
    for line in sys.stdin:
        parsed = EnrollmentParser.parse(line)
        if not parsed:
            continue

        course_id = parsed.get("course_id")
        total_score = parsed.get("total_score")
        if course_id is None or total_score is None:
            continue

        label = "Pass" if total_score >= 4.0 else "Fail"
        sys.stdout.write(f"{course_id}\t{label}\n")


if __name__ == "__main__":
    main()

