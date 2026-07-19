#!/usr/bin/env python3
"""reducer/semester_count.py

Hadoop Streaming - Count students per semester

Reducer (also usable as Combiner):
- Input: semester\t1
- Output: semester\tTOTAL

Optimized for sorted input by key.
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

