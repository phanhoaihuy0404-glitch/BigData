#!/usr/bin/env python3
"""mapper/semester_count.py

Hadoop Streaming - Count students per semester

Input : Enrollment.csv (9 columns) with header
        EnrollmentID,StudentID,CourseID,Semester,Year,MidtermScore,FinalScore,TotalScore,LetterGrade
Output: semester\t1

Rules:
- Read from sys.stdin
- Parse CSV manually (no external dependencies)
- Semester is at column index 3
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

