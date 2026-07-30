import random

import pandas as pd

from config import *

students = pd.read_csv(DATA_FOLDER / "Student.csv")
courses = pd.read_csv(DATA_FOLDER / "Course.csv")


def get_grade(score):

    if score >= 8.5:
        return "A"

    elif score >= 7:
        return "B"

    elif score >= 5.5:
        return "C"

    elif score >= 4:
        return "D"

    return "F"


rows = []

used = set()

enrollment_id = 1

course_ids = list(courses["CourseID"])

student_ids = list(students["StudentID"])

while len(rows) < NUM_ENROLLMENTS:

    student = random.choice(student_ids)

    course = random.choice(course_ids)

    if (student, course) in used:
        continue

    used.add((student, course))

    midterm = round(random.uniform(3, 10), 1)

    final = round(random.uniform(3, 10), 1)

    total = round(midterm * 0.4 + final * 0.6, 1)

    rows.append({

        "EnrollmentID": enrollment_id,

        "StudentID": student,

        "CourseID": course,

        "Semester": SEMESTER,

        "Year": YEAR,

        "MidtermScore": midterm,

        "FinalScore": final,

        "TotalScore": total,

        "LetterGrade": get_grade(total)

    })

    enrollment_id += 1

df = pd.DataFrame(rows)

output_file = DATA_FOLDER / "Enrollment.csv"

df.to_csv(
    output_file,
    index=False
)

print("=" * 50)
print("Enrollment Dataset Generated")
print("=" * 50)
print(f"Total Enrollments : {len(df)}")
print(f"Output File       : {output_file}")