#!/usr/bin/env python3
"""reducer/semester_count_reducer.py

Hadoop Streaming - Count students per semester (reducer)

Input format:
  semester\t1   (from mapper)

Output format:
  semester\tTOTAL

This reducer is intentionally separate from semester_count.py so you can
use semester_count_reducer.py as the main reducer, and semester_count.py
as a combiner if desired.

Optimized:
- Assumes input sorted by semester key (streaming aggregation).
"""

import sys


def main():
    current_semester = None
    total = 0

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            semester, value = raw.split("\t", 1)
        except ValueError:
            continue

        try:
            v = int(value)
        except (ValueError, TypeError):
            continue

        if current_semester is None:
            current_semester = semester
            total = v
        elif semester == current_semester:
            total += v
        else:
            sys.stdout.write(f"{current_semester}\t{total}\n")
            current_semester = semester
            total = v

    if current_semester is not None:
        sys.stdout.write(f"{current_semester}\t{total}\n")


if __name__ == "__main__":
    main()

