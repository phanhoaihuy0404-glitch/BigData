#!/usr/bin/env python3
"""
Mapper for counting students per semester.

Input : CSV line from Enrollment.csv
Output: semester<TAB>1
"""

import sys


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Parse CSV line (simple split by comma)
        columns = line.split(",")

        # Skip header
        if columns[0].strip().lower() == "enrollmentid":
            continue

        # Need exactly 9 columns
        if len(columns) < 9:
            continue

        semester = columns[3].strip()
        if semester:
            sys.stdout.write(f"{semester}\t1\n")


if __name__ == "__main__":
    main()

