#!/usr/bin/env python3
"""
Mapper for counting students per course (CourseID).

Input : CSV file with header
        EnrollmentID,StudentID,CourseID,Semester,Year,MidtermScore,FinalScore,TotalScore,LetterGrade
Output: CourseID<TAB>1   (one record per enrollment = one student in that course)
"""

import sys
import csv
from io import StringIO

def main():
    reader = csv.reader(sys.stdin)
    header_skipped = False

    for row in reader:
        # Skip empty lines
        if not row:
            continue

        # Skip the header row
        if not header_skipped:
            header_skipped = True
            # If the first column looks like a header, skip it
            if row[0].strip().lower() == "enrollmentid":
                continue

        # Expected columns: EnrollmentID, StudentID, CourseID, ...
        # CourseID is at index 2 (0-based)
        if len(row) >= 3:
            course_id = row[2].strip()
            student_id = row[1].strip()
            # Only emit if both CourseID and StudentID are present
            if course_id and student_id:
                # Output: CourseID<TAB>1
                print(f"{course_id}\t1")

if __name__ == "__main__":
    main()