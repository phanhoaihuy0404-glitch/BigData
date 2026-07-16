"""
Database Validation Script
===========================
Validates data integrity of processed CSV files before MongoDB import.

Checks:
  - Primary Key uniqueness
  - Foreign Key referential integrity
  - Score ranges and formulas
  - LetterGrade correctness
  - Missing values
  - Duplicate records
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROC_DIR = Path("data/processed")

# ──────────────────────────────────────────────
# Load all collections
# ──────────────────────────────────────────────
dept    = pd.read_csv(PROC_DIR / "Department.csv")
cls     = pd.read_csv(PROC_DIR / "Class.csv")
teacher = pd.read_csv(PROC_DIR / "Teacher.csv")
student = pd.read_csv(PROC_DIR / "Student.csv")
course  = pd.read_csv(PROC_DIR / "Course.csv")
enroll  = pd.read_csv(PROC_DIR / "Enrollment.csv")
att     = pd.read_csv(PROC_DIR / "Attendance.csv")

results = []
all_pass = True

def test(name, condition, detail=""):
    global all_pass
    status = "PASS" if condition else "FAIL"
    if not condition:
        all_pass = False
    label = f"{name:.<55} {status}"
    if detail and not condition:
        label += f"  [{detail}]"
    results.append(label)

# ══════════════════════════════════════════════
# PRIMARY KEY VALIDATION
# ══════════════════════════════════════════════
print("=" * 70)
print("DATABASE VALIDATION")
print("=" * 70)

print("\n" + "=" * 70)
print("PRIMARY KEY VALIDATION")
print("=" * 70)

test("Department PK (DepartmentID)", dept["DepartmentID"].is_unique)
test("Class PK (ClassID)", cls["ClassID"].is_unique)
test("Teacher PK (TeacherID)", teacher["TeacherID"].is_unique)
test("Student PK (StudentID)", student["StudentID"].is_unique)
test("Course PK (CourseID)", course["CourseID"].is_unique)
test("Enrollment PK (EnrollmentID)", enroll["EnrollmentID"].is_unique)
test("Attendance PK (AttendanceID)", att["AttendanceID"].is_unique)

# ══════════════════════════════════════════════
# FOREIGN KEY VALIDATION
# ══════════════════════════════════════════════
print("\n" + "=" * 70)
print("FOREIGN KEY VALIDATION")
print("=" * 70)

# Student → Class
fk = student["ClassID"].isin(cls["ClassID"])
test("Student -> Class", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Class → Department
fk = cls["DepartmentID"].isin(dept["DepartmentID"])
test("Class -> Department", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Course → Department
fk = course["DepartmentID"].isin(dept["DepartmentID"])
test("Course -> Department", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Course → Teacher
fk = course["TeacherID"].isin(teacher["TeacherID"])
test("Course -> Teacher", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Enrollment → Student
fk = enroll["StudentID"].isin(student["StudentID"])
test("Enrollment -> Student", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Enrollment → Course
fk = enroll["CourseID"].isin(course["CourseID"])
test("Enrollment -> Course", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Attendance → Student
fk = att["StudentID"].isin(student["StudentID"])
test("Attendance -> Student", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# Attendance → Course
fk = att["CourseID"].isin(course["CourseID"])
test("Attendance -> Course", fk.all(),
     f"{fk.sum()}/{len(fk)} valid, {(~fk).sum()} invalid")

# ══════════════════════════════════════════════
# SCORE VALIDATION
# ══════════════════════════════════════════════
print("\n" + "=" * 70)
print("SCORE VALIDATION")
print("=" * 70)

# MidtermScore range 0-10
in_range = enroll["MidtermScore"].between(0, 10, inclusive="both")
test("MidtermScore 0-10", in_range.all(),
     f"{in_range.sum()}/{len(in_range)} in range, {(~in_range).sum()} out")

# FinalScore range 0-10
in_range = enroll["FinalScore"].between(0, 10, inclusive="both")
test("FinalScore 0-10", in_range.all(),
     f"{in_range.sum()}/{len(in_range)} in range, {(~in_range).sum()} out")

# TotalScore = 0.4 * Midterm + 0.6 * Final
tolerance = 0.02
expected_total = round(0.4 * enroll["MidtermScore"] + 0.6 * enroll["FinalScore"], 2)
total_match = abs(enroll["TotalScore"] - expected_total) < tolerance
test("TotalScore = 0.4*Midterm + 0.6*Final", total_match.all(),
     f"{total_match.sum()}/{len(total_match)} match, {(~total_match).sum()} mismatch")

# LetterGrade matches TotalScore
def expected_grade(score):
    if score >= 8.5:
        return "A"
    elif score >= 7.0:
        return "B"
    elif score >= 5.5:
        return "C"
    elif score >= 4.0:
        return "D"
    else:
        return "F"

expected_grades = enroll["TotalScore"].apply(expected_grade)
grade_match = enroll["LetterGrade"] == expected_grades
test("LetterGrade matches TotalScore", grade_match.all(),
     f"{grade_match.sum()}/{len(grade_match)} match, {(~grade_match).sum()} mismatch")

# ══════════════════════════════════════════════
# DATA QUALITY
# ══════════════════════════════════════════════
print("\n" + "=" * 70)
print("DATA QUALITY")
print("=" * 70)

# No missing values in PK columns
test("Department.DepartmentID no nulls", dept["DepartmentID"].notna().all())
test("Class.ClassID no nulls", cls["ClassID"].notna().all())
test("Teacher.TeacherID no nulls", teacher["TeacherID"].notna().all())
test("Student.StudentID no nulls", student["StudentID"].notna().all())
test("Course.CourseID no nulls", course["CourseID"].notna().all())
test("Enrollment.EnrollmentID no nulls", enroll["EnrollmentID"].notna().all())
test("Attendance.AttendanceID no nulls", att["AttendanceID"].notna().all())

# No missing values in FK columns
test("Student.ClassID no nulls", student["ClassID"].notna().all())
test("Class.DepartmentID no nulls", cls["DepartmentID"].notna().all())
test("Course.DepartmentID no nulls", course["DepartmentID"].notna().all())
test("Course.TeacherID no nulls", course["TeacherID"].notna().all())
test("Enrollment.StudentID no nulls", enroll["StudentID"].notna().all())
test("Enrollment.CourseID no nulls", enroll["CourseID"].notna().all())
test("Attendance.StudentID no nulls", att["StudentID"].notna().all())
test("Attendance.CourseID no nulls", att["CourseID"].notna().all())

# No missing values in score fields
test("Enrollment.MidtermScore no nulls", enroll["MidtermScore"].notna().all())
test("Enrollment.FinalScore no nulls", enroll["FinalScore"].notna().all())
test("Enrollment.TotalScore no nulls", enroll["TotalScore"].notna().all())
test("Enrollment.LetterGrade no nulls", enroll["LetterGrade"].notna().all())

# No duplicate primary keys (already checked above, but verify count)
test("No duplicate DepartmentID", dept["DepartmentID"].duplicated().sum() == 0)
test("No duplicate ClassID", cls["ClassID"].duplicated().sum() == 0)
test("No duplicate TeacherID", teacher["TeacherID"].duplicated().sum() == 0)
test("No duplicate StudentID", student["StudentID"].duplicated().sum() == 0)
test("No duplicate CourseID", course["CourseID"].duplicated().sum() == 0)
test("No duplicate EnrollmentID", enroll["EnrollmentID"].duplicated().sum() == 0)
test("No duplicate AttendanceID", att["AttendanceID"].duplicated().sum() == 0)

# ══════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════
print("\n" + "=" * 70)
print("REPORT")
print("=" * 70)

for r in results:
    print(r)

print("\n" + "=" * 70)
if all_pass:
    print("DATABASE VALIDATION PASSED")
else:
    print("DATABASE VALIDATION FAILED")
print("=" * 70)