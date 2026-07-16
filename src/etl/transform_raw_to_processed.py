"""
ETL Script: Transform Raw Kaggle Dataset → Processed Schema
=============================================================
Transforms data/raw/*.csv files into the redesigned schema
under data/processed/*.csv

New collections:
  - Department
  - Class
  - Teacher
  - Student
  - Course
  - Enrollment
  - Attendance

Removed:
  - Feedback (not in processed)
  - Grades  (not in processed; grades.csv is only an ETL source)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
RAW_DIR   = Path("data/raw")
PROC_DIR  = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────
# 1. Load raw data
# ──────────────────────────────────────────────
students_raw    = pd.read_csv(RAW_DIR / "students.csv")
courses_raw     = pd.read_csv(RAW_DIR / "courses.csv")
enrollments_raw = pd.read_csv(RAW_DIR / "enrollments.csv")
attendance_raw  = pd.read_csv(RAW_DIR / "attendance.csv")
# grades.csv — ETL source only, not a target collection
# feedback.csv — removed from schema

print("=" * 70)
print("ETL: Raw → Processed Schema Transformation")
print("=" * 70)

# ──────────────────────────────────────────────
# 2. Create Department collection
# ──────────────────────────────────────────────
unique_departments = sorted(courses_raw["Department"].unique())
dept_map = {}
department_rows = []
for i, dept_name in enumerate(unique_departments, start=1):
    dept_id = f"DEPT{i:03d}"
    dept_map[dept_name] = dept_id
    department_rows.append({
        "DepartmentID": dept_id,
        "DepartmentName": dept_name
    })

department_df = pd.DataFrame(department_rows)
department_df.to_csv(PROC_DIR / "Department.csv", index=False)
print(f"\n[Department] Created {len(department_df)} departments")
print(department_df.to_string(index=False))

# ──────────────────────────────────────────────
# 3. Create Teacher collection
# ──────────────────────────────────────────────
# Build teacher_map from lexicographic order to preserve existing TeacherIDs
unique_instructors_lex = sorted(courses_raw["Instructor"].unique())
teacher_map = {}
teacher_rows = []
np.random.seed(7)  # reproducible for phone numbers
for i, instr_name in enumerate(unique_instructors_lex, start=1):
    teacher_id = f"TCH{i:03d}"
    teacher_map[instr_name] = teacher_id
    
    # Generate realistic email: teacher01@university.edu
    num_str = f"{i:02d}"
    email = f"teacher{num_str}@university.edu"
    
    # Generate realistic phone: (XXX) XXX-XXXX
    area = np.random.randint(200, 999)
    exch = np.random.randint(200, 999)
    line = np.random.randint(1000, 9999)
    phone = f"({area}) {exch}-{line}"
    
    teacher_rows.append({
        "TeacherID": teacher_id,
        "TeacherName": instr_name,
        "Email": email,
        "Phone": phone
    })

# Sort by TeacherName numerically before writing (Instructor 1, Instructor 2, ..., Instructor 50)
teacher_df = pd.DataFrame(teacher_rows)
teacher_df["_sort_key"] = teacher_df["TeacherName"].str.extract(r"(\d+)").astype(int)
teacher_df = teacher_df.sort_values("_sort_key").drop(columns="_sort_key").reset_index(drop=True)
teacher_df.to_csv(PROC_DIR / "Teacher.csv", index=False)
print(f"\n[Teacher] Created {len(teacher_df)} teachers")
print(teacher_df.to_string(index=False))

# ──────────────────────────────────────────────
# 4. Create Class collection
# ──────────────────────────────────────────────
# Map majors (from Student.Major) to departments
major_to_dept = {
    "Computer Science": "Computer Science",
    "Physics":          "Physics",
    "Biology":          "Biology",
    "Mathematics":      "Mathematics"
}

# Define realistic class names per department
dept_class_suffix = {
    "Computer Science": ["SE01", "SE02", "AI01", "AI02", "CS01", "CS02"],
    "Physics":          ["PHY01", "PHY02", "PHY03"],
    "Biology":          ["BIO01", "BIO02", "BIO03"],
    "Mathematics":      ["MATH01", "MATH02", "MATH03"]
}

# Assign each student a class based on their major
# We split students per major into groups, each group gets a class
np.random.seed(42)  # reproducible

class_rows = []
class_id_counter = 1
student_class_assignment = {}  # StudentID → ClassID

for major in sorted(students_raw["Major"].unique()):
    dept_name = major_to_dept.get(major, "General")
    dept_id = dept_map[dept_name]
    suffixes = dept_class_suffix.get(major, ["GEN01"])
    
    # Get all students with this major
    major_students = students_raw[students_raw["Major"] == major]
    student_ids = major_students["StudentID"].tolist()
    np.random.shuffle(student_ids)
    
    # Split into groups
    n_classes = min(len(suffixes), len(student_ids))
    if n_classes == 0:
        n_classes = 1
    groups = np.array_split(student_ids, n_classes)
    
    for idx, group in enumerate(groups):
        class_id = f"CLASS{class_id_counter:03d}"
        class_name = f"{suffixes[idx]}"
        class_rows.append({
            "ClassID": class_id,
            "ClassName": class_name,
            "DepartmentID": dept_id
        })
        for sid in group:
            student_class_assignment[sid] = class_id
        class_id_counter += 1

class_df = pd.DataFrame(class_rows)
class_df.to_csv(PROC_DIR / "Class.csv", index=False)
print(f"\n[Class] Created {len(class_df)} classes")
print(class_df.to_string(index=False))

# ──────────────────────────────────────────────
# 5. Create Student collection (updated schema)
# ──────────────────────────────────────────────
student_rows = []
for _, row in students_raw.iterrows():
    sid = row["StudentID"]
    student_rows.append({
        "StudentID": sid,
        "FirstName": row["FirstName"],
        "LastName":  row["LastName"],
        "Gender":    row["Gender"],
        "DateOfBirth": row["DateOfBirth"],
        "ClassID":   student_class_assignment.get(sid, "CLASS001")
    })

student_df = pd.DataFrame(student_rows)
student_df.to_csv(PROC_DIR / "Student.csv", index=False)
print(f"\n[Student] Created {len(student_df)} students (Major removed, ClassID added)")

# ──────────────────────────────────────────────
# 6. Create Course collection (updated schema)
# ──────────────────────────────────────────────
course_rows = []
for _, row in courses_raw.iterrows():
    course_rows.append({
        "CourseID":     row["CourseID"],
        "CourseName":   row["CourseName"],
        "DepartmentID": dept_map[row["Department"]],
        "Credits":      row["Credits"],
        "TeacherID":    teacher_map[row["Instructor"]]
    })

course_df = pd.DataFrame(course_rows)
course_df.to_csv(PROC_DIR / "Course.csv", index=False)
print(f"\n[Course] Created {len(course_df)} courses (Department→DepartmentID, Instructor→TeacherID)")
print(course_df.head().to_string(index=False))

# ──────────────────────────────────────────────
# 7. Redesign Enrollment collection
# ──────────────────────────────────────────────
# The raw grades.csv has very little overlap with enrollments.csv.
# We generate Midterm and Final scores based on the existing LetterGrade
# from enrollments.csv, then compute TotalScore and LetterGrade.

# Score ranges per letter grade (scores out of 10):
# A  (8.5-10.0) → Midterm 7.5-10, Final 8.5-10
# B  (7.0-8.4)  → Midterm 6.5-8.5, Final 7.0-8.5
# C  (5.5-6.9)  → Midterm 5.0-7.0, Final 5.5-7.0
# D  (4.0-5.4)  → Midterm 3.5-5.5, Final 4.0-5.5
# F  (0.0-3.9)  → Midterm 2.0-4.0, Final 1.0-4.0

grade_ranges = {
    "A": {"mt": (7.5, 10.0), "ft": (8.5, 10.0)},
    "B": {"mt": (6.5, 8.5),  "ft": (7.0, 8.5)},
    "C": {"mt": (5.0, 7.0),  "ft": (5.5, 7.0)},
    "D": {"mt": (3.5, 5.5),  "ft": (4.0, 5.5)},
    "F": {"mt": (2.0, 4.0),  "ft": (1.0, 4.0)}
}

np.random.seed(123)  # reproducible

enrollment_rows = []
for _, row in enrollments_raw.iterrows():
    letter = row["Grade"]
    ranges = grade_ranges.get(letter, grade_ranges["C"])
    
    # Generate midterm and final scores within the grade range
    mt_lo, mt_hi = ranges["mt"]
    ft_lo, ft_hi = ranges["ft"]
    
    midterm_val = round(np.random.uniform(mt_lo, mt_hi), 1)
    final_val   = round(np.random.uniform(ft_lo, ft_hi), 1)
    
    # Compute TotalScore = 0.4 * Midterm + 0.6 * Final
    total_val = round(0.4 * midterm_val + 0.6 * final_val, 2)
    
    # Compute LetterGrade from TotalScore
    if total_val >= 8.5:
        letter_grade = "A"
    elif total_val >= 7.0:
        letter_grade = "B"
    elif total_val >= 5.5:
        letter_grade = "C"
    elif total_val >= 4.0:
        letter_grade = "D"
    else:
        letter_grade = "F"
    
    enrollment_rows.append({
        "EnrollmentID": row["EnrollmentID"],
        "StudentID":    row["StudentID"],
        "CourseID":     row["CourseID"],
        "Semester":     row["Semester"],
        "Year":         row["Year"],
        "MidtermScore": midterm_val,
        "FinalScore":   final_val,
        "TotalScore":   total_val,
        "LetterGrade":  letter_grade
    })

enrollment_df = pd.DataFrame(enrollment_rows)
enrollment_df.to_csv(PROC_DIR / "Enrollment.csv", index=False)
print(f"\n[Enrollment] Created {len(enrollment_df)} enrollments (with MidtermScore, FinalScore, TotalScore, LetterGrade)")
print(enrollment_df.head(10).to_string(index=False))

# Report score coverage
has_midterm = enrollment_df["MidtermScore"].notna().sum()
has_final   = enrollment_df["FinalScore"].notna().sum()
has_total   = enrollment_df["TotalScore"].notna().sum()
print(f"\n    - With MidtermScore: {has_midterm}/{len(enrollment_df)}")
print(f"    - With FinalScore:   {has_final}/{len(enrollment_df)}")
print(f"    - With TotalScore:   {has_total}/{len(enrollment_df)}")
print(f"    - LetterGrade distribution:")
print(enrollment_df["LetterGrade"].value_counts().sort_index().to_string())

# ──────────────────────────────────────────────
# 8. Create Attendance collection (unchanged)
# ──────────────────────────────────────────────
attendance_df = attendance_raw.copy()
attendance_df.to_csv(PROC_DIR / "Attendance.csv", index=False)
print(f"\n[Attendance] Created {len(attendance_df)} records (unchanged schema)")

# ──────────────────────────────────────────────
# 9. Summary
# ──────────────────────────────────────────────
print("\n" + "=" * 70)
print("ETL COMPLETE")
print("=" * 70)
print(f"\nFiles created in {PROC_DIR}/:")
for f in sorted(PROC_DIR.glob("*.csv")):
    print(f"  ✓ {f.name}")

print(f"\nCollections NOT created (removed from schema):")
print(f"  ✗ Feedback (removed)")
print(f"  ✗ Grades   (removed; used only as ETL source)")

print(f"\nSummary of schema changes:")
print(f"  + Department  (NEW) — normalized from courses.Department")
print(f"  + Class       (NEW) — generated from student majors")
print(f"  + Teacher     (NEW) — normalized from courses.Instructor")
print(f"  ~ Student     (UPDATED) — Major dropped, ClassID added")
print(f"  ~ Course      (UPDATED) — Department→DepartmentID, Instructor→TeacherID")
print(f"  ~ Enrollment  (UPDATED) — Grade→MidtermScore+FinalScore+TotalScore+LetterGrade")
print(f"  = Attendance  (UNCHANGED)")