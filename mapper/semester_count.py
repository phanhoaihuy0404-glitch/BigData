#!/usr/bin/env python3
"""mapper/semester_count.py

Hadoop Streaming - Count students per semester

Input : Enrollment.csv (9 columns) with header
Output: semester\t1

Rules:
- Read from sys.stdin
- Use EnrollmentParser.parse(line)
"""

import sys

# Ensure local import works when executed by Hadoop Streaming
# (Hadoop usually runs the script from its own working dir)
try:
    from parser.enrollment_parser import EnrollmentParser
except ImportError:
    # Fallback: allow running directly from repo root
    from parser.enrollment_parser import EnrollmentParser  # type: ignore


def main():
    for line in sys.stdin:
        parsed = EnrollmentParser.parse(line)
        if not parsed:
            continue
        semester = parsed.get("semester")
        if semester:
            sys.stdout.write(f"{semester}\t1\n")


if __name__ == "__main__":
    main()

