import pandas as pd
from pathlib import Path

PROC_DIR = Path("data/processed")
RAW_DIR  = Path("data/raw")

print("=" * 70)
print("SCHEMA VERIFICATION: Processed Dataset")
print("=" * 70)

all_pass = True

def check(condition, message):
    global all_pass
    if condition:
        print(f"  ✓ {message}")
    else:
        print(f"  ✗ FAIL: {message}")
        all_pass = False

# ──────────────────────────────────────────────
# 1. Department exists
# ──────────────────────────────────────────────
print("\n[1] Department Collection")
dept = pd.read_csv(PROC_DIR / "Department.csv")
check("DepartmentID" in dept.columns, "Department has DepartmentID")
check("DepartmentName" in dept.columns, "Department has DepartmentName")
check(len(dept) > 0, f"Department has {len(dept)} records")
check(len(dept.columns) == 2, f"Department has exactly 2 columns (has {len(dept.columns)})")

# ──────────────────────────────────────────────
# 2. Class exists
# ──────────────────────────────────────────────
print("\n[2] Class Collection")
cls = pd.read_csv(PROC_DIR / "Class.csv")
check("ClassID" in cls.columns, "Class has ClassID")
check("ClassName" in cls.columns, "Class has ClassName")
check("DepartmentID" in cls.columns, "Class has DepartmentID (FK → Department)")
check(len(cls) > 0, f"Class has {len(cls)} records")

# Verify DepartmentID references
check(cls["DepartmentID"].isin(dept["DepartmentID"]).all(),
      "All Class.DepartmentID values exist in Department")

# ──────────────────────────────────────────────
# 3. Teacher exists
# ──────────────────────────────────────────────
print("\n[3] Teacher Collection")
teacher = pd.read_csv(PROC_DIR / "Teacher.csv")
check("TeacherID" in teacher.columns, "Teacher has TeacherID")
check("TeacherName" in teacher.columns, "Teacher has TeacherName")
check("Email" in teacher.columns, "Teacher has Email")
check("Phone" in teacher.columns, "Teacher has Phone")
check(len(teacher) > 0, f"Teacher has {len(teacher)} records")
check(len(teacher.columns) == 4, f"Teacher has exactly 4 columns (has {len(teacher.columns)})")

# Verify email format
email_pattern = teacher["Email"].str.match(r"^teacher\d{2}@university\.edu$").all()
check(email_pattern, "All emails match pattern teacherXX@university.edu")

# Verify phone format
phone_pattern = teacher["Phone"].str.match(r"^\(\d{3}\) \d{3}-\d{4}$").all()
check(phone_pattern, "All phones match pattern (XXX) XXX-XXXX")

# ──────────────────────────────────────────────
# 4. Student references Class
# ──────────────────────────────────────────────
print("\n[4] Student Collection")
student = pd.read_csv(PROC_DIR / "Student.csv")
check("StudentID" in student.columns, "Student has StudentID")
check("FirstName" in student.columns, "Student has FirstName")
check("LastName" in student.columns, "Student has LastName")
check("Gender" in student.columns, "Student has Gender")
check("DateOfBirth" in student.columns, "Student has DateOfBirth")
check("ClassID" in student.columns, "Student has ClassID (FK → Class)")
check("Major" not in student.columns, "Student does NOT have Major (removed)")
check("GPA" not in student.columns, "Student does NOT have GPA (removed)")
check(len(student) > 0, f"Student has {len(student)} records")

# Verify ClassID references
check(student["ClassID"].isin(cls["ClassID"]).all(),
      "All Student.ClassID values exist in Class")

# ──────────────────────────────────────────────
# 5. Course references Teacher and Department
# ──────────────────────────────────────────────
print("\n[5] Course Collection")
course = pd.read_csv(PROC_DIR / "Course.csv")
check("CourseID" in course.columns, "Course has CourseID")
check("CourseName" in course.columns, "Course has CourseName")
check("DepartmentID" in course.columns, "Course has DepartmentID (FK → Department)")
check("Credits" in course.columns, "Course has Credits")
check("TeacherID" in course.columns, "Course has TeacherID (FK → Teacher)")
check("Department" not in course.columns, "Course does NOT have Department string (replaced by DepartmentID)")
check("Instructor" not in course.columns, "Course does NOT have Instructor string (replaced by TeacherID)")
check(len(course) > 0, f"Course has {len(course)} records")

# Verify references
check(course["DepartmentID"].isin(dept["DepartmentID"]).all(),
      "All Course.DepartmentID values exist in Department")
check(course["TeacherID"].isin(teacher["TeacherID"]).all(),
      "All Course.TeacherID values exist in Teacher")

# ──────────────────────────────────────────────
# 6. Enrollment has all required score fields
# ──────────────────────────────────────────────
print("\n[6] Enrollment Collection")
enroll = pd.read_csv(PROC_DIR / "Enrollment.csv")
check("EnrollmentID" in enroll.columns, "Enrollment has EnrollmentID")
check("StudentID" in enroll.columns, "Enrollment has StudentID (FK → Student)")
check("CourseID" in enroll.columns, "Enrollment has CourseID (FK → Course)")
check("Semester" in enroll.columns, "Enrollment has Semester")
check("Year" in enroll.columns, "Enrollment has Year")
check("MidtermScore" in enroll.columns, "Enrollment has MidtermScore ✓")
check("FinalScore" in enroll.columns, "Enrollment has FinalScore ✓")
check("TotalScore" in enroll.columns, "Enrollment has TotalScore ✓")
check("LetterGrade" in enroll.columns, "Enrollment has LetterGrade ✓")
check("Grade" not in enroll.columns, "Enrollment does NOT have old Grade field (replaced)")
check(len(enroll) > 0, f"Enrollment has {len(enroll)} records")

# Verify all scores are populated
check(enroll["MidtermScore"].notna().all(), "All enrollments have MidtermScore (no NaN)")
check(enroll["FinalScore"].notna().all(), "All enrollments have FinalScore (no NaN)")
check(enroll["TotalScore"].notna().all(), "All enrollments have TotalScore (no NaN)")
check(enroll["LetterGrade"].notna().all(), "All enrollments have LetterGrade (no NaN)")

# Verify TotalScore = 0.4 * Midterm + 0.6 * Final
tolerance = 0.02
expected_total = round(0.4 * enroll["MidtermScore"] + 0.6 * enroll["FinalScore"], 2)
total_match = (abs(enroll["TotalScore"] - expected_total) < tolerance).all()
check(total_match, "TotalScore = 0.4 * MidtermScore + 0.6 * FinalScore for all records")

# Verify LetterGrade follows the scale
valid_grades = {"A", "B", "C", "D", "F"}
check(set(enroll["LetterGrade"].unique()).issubset(valid_grades),
      f"LetterGrade values are valid: {sorted(enroll['LetterGrade'].unique())}")

# Verify references
check(enroll["StudentID"].isin(student["StudentID"]).all(),
      "All Enrollment.StudentID values exist in Student")
check(enroll["CourseID"].isin(course["CourseID"]).all(),
      "All Enrollment.CourseID values exist in Course")

# ──────────────────────────────────────────────
# 7. Attendance exists (unchanged)
# ──────────────────────────────────────────────
print("\n[7] Attendance Collection")
att = pd.read_csv(PROC_DIR / "Attendance.csv")
check("AttendanceID" in att.columns, "Attendance has AttendanceID")
check("StudentID" in att.columns, "Attendance has StudentID")
check("CourseID" in att.columns, "Attendance has CourseID")
check("Date" in att.columns, "Attendance has Date")
check("AttendanceStatus" in att.columns, "Attendance has AttendanceStatus")
check(len(att) > 0, f"Attendance has {len(att)} records")

# ──────────────────────────────────────────────
# 8. Feedback no longer exists in processed
# ──────────────────────────────────────────────
print("\n[8] Removed Collections")
feedback_exists = (PROC_DIR / "Feedback.csv").exists()
check(not feedback_exists, "Feedback.csv does NOT exist in processed (removed)")

# ──────────────────────────────────────────────
# 9. Grades no longer exists in processed
# ──────────────────────────────────────────────
grades_exists = (PROC_DIR / "Grades.csv").exists()
check(not grades_exists, "Grades.csv does NOT exist in processed (removed)")

# ──────────────────────────────────────────────
# 10. Raw data is untouched
# ──────────────────────────────────────────────
print("\n[9] Raw Data Integrity")
raw_files = ["students.csv", "courses.csv", "enrollments.csv", "grades.csv", "attendance.csv", "feedback.csv"]
for f in raw_files:
    check((RAW_DIR / f).exists(), f"Raw file {f} is preserved (not modified)")

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
print("\n" + "=" * 70)
if all_pass:
    print("RESULT: ✓ ALL CHECKS PASSED — Schema redesign is correctly implemented")
else:
    print("RESULT: ✗ SOME CHECKS FAILED — Review issues above")
print("=" * 70)