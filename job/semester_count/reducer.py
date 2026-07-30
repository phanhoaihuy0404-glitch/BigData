#!/usr/bin/env python3
"""
Reducer for counting students per semester.

Input : semester<TAB>1   (from mapper, sorted by semester)
Output: semester<TAB>TOTAL
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

