import pandas as pd

from config import *

COURSE_INFO = [
    ("DS", "Data Structure", 3),
    ("DB", "Database Systems", 3),
    ("OS", "Operating Systems", 4),
    ("CN", "Computer Networks", 3),
    ("OOP", "Object Oriented Programming", 3),
    ("SE", "Software Engineering", 3),
    ("AI", "Artificial Intelligence", 3),
    ("ML", "Machine Learning", 3),
    ("DM", "Data Mining", 3),
    ("WP", "Web Programming", 3),
]

courses = []

for code, name, credit in COURSE_INFO:

    for section in range(1, 4):

        courses.append({

            "CourseID": f"251{code}{section}",

            "CourseName": name,

            "Credits": credit

        })

df = pd.DataFrame(courses)

output_file = DATA_FOLDER / "Course.csv"

df.to_csv(
    output_file,
    index=False
)

print("=" * 50)
print("Course Dataset Generated")
print("=" * 50)
print(f"Total Courses : {len(df)}")
print(f"Output File   : {output_file}")