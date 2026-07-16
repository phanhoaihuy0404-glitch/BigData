"""
MongoDB Query Examples
======================
Read-only queries to verify MongoDB contains correct data.

All queries use mongodb/config.py for connection settings.
No data is modified — only read operations.
"""

from mongodb.connect import get_database


def query_1_count_all(db):
    """Count documents in every collection."""
    print("\n" + "=" * 25)
    print("QUERY 1")
    print("=" * 25)
    collections = ["Department", "Class", "Teacher", "Student",
                   "Course", "Enrollment", "Attendance"]
    for name in collections:
        count = db[name].count_documents({})
        print(f"{name:.<15} {count}")


def query_2_first_5_students(db):
    """List first 5 students."""
    print("\n" + "=" * 25)
    print("QUERY 2")
    print("=" * 25)
    print("First 5 Students:")
    students = db["Student"].find().limit(5)
    for s in students:
        print(f"  {s['StudentID']} | {s['FirstName']} {s['LastName']} | {s['Gender']} | Class: {s['ClassID']}")


def query_3_first_5_courses(db):
    """List first 5 courses."""
    print("\n" + "=" * 25)
    print("QUERY 3")
    print("=" * 25)
    print("First 5 Courses:")
    courses = db["Course"].find().limit(5)
    for c in courses:
        print(f"  {c['CourseID']} | {c['CourseName']} | Dept: {c['DepartmentID']} | Teacher: {c['TeacherID']}")


def query_4_first_5_teachers(db):
    """List first 5 teachers."""
    print("\n" + "=" * 25)
    print("QUERY 4")
    print("=" * 25)
    print("First 5 Teachers:")
    teachers = db["Teacher"].find().limit(5)
    for t in teachers:
        print(f"  {t['TeacherID']} | {t['TeacherName']} | {t['Email']} | {t['Phone']}")


def query_5_students_by_class(db):
    """Count students grouped by ClassID."""
    print("\n" + "=" * 25)
    print("QUERY 5")
    print("=" * 25)
    print("Students by ClassID:")
    pipeline = [
        {"$group": {"_id": "$ClassID", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = db["Student"].aggregate(pipeline)
    for r in results:
        print(f"  {r['_id']:.<20} {r['count']} students")


def query_6_courses_by_department(db):
    """Count courses grouped by DepartmentID."""
    print("\n" + "=" * 25)
    print("QUERY 6")
    print("=" * 25)
    print("Courses by DepartmentID:")
    pipeline = [
        {"$group": {"_id": "$DepartmentID", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = db["Course"].aggregate(pipeline)
    for r in results:
        print(f"  {r['_id']:.<20} {r['count']} courses")


def query_7_average_total_score(db):
    """Average TotalScore across all enrollments."""
    print("\n" + "=" * 25)
    print("QUERY 7")
    print("=" * 25)
    pipeline = [
        {"$group": {"_id": None, "avgScore": {"$avg": "$TotalScore"}}}
    ]
    results = list(db["Enrollment"].aggregate(pipeline))
    if results:
        avg = round(results[0]["avgScore"], 2)
        print(f"Average TotalScore: {avg}")


def query_8_grade_distribution(db):
    """Count enrollments per letter grade."""
    print("\n" + "=" * 25)
    print("QUERY 8")
    print("=" * 25)
    print("Grade Distribution:")
    pipeline = [
        {"$group": {"_id": "$LetterGrade", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = db["Enrollment"].aggregate(pipeline)
    grade_order = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}
    sorted_results = sorted(results, key=lambda r: grade_order.get(r["_id"], 99))
    for r in sorted_results:
        print(f"  {r['_id']}: {r['count']}")


def query_9_top_10_students(db):
    """Top 10 students by TotalScore (show StudentID and TotalScore)."""
    print("\n" + "=" * 25)
    print("QUERY 9")
    print("=" * 25)
    print("Top 10 Students by TotalScore:")
    pipeline = [
        {"$sort": {"TotalScore": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "StudentID": 1, "TotalScore": 1, "LetterGrade": 1}}
    ]
    results = db["Enrollment"].aggregate(pipeline)
    for i, r in enumerate(results, start=1):
        print(f"  {i:>2}. Student {r['StudentID']:>5}  Score: {r['TotalScore']:>5}  Grade: {r['LetterGrade']}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    db = get_database()
    print(f"Database: {db.name}\n")

    query_1_count_all(db)
    query_2_first_5_students(db)
    query_3_first_5_courses(db)
    query_4_first_5_teachers(db)
    query_5_students_by_class(db)
    query_6_courses_by_department(db)
    query_7_average_total_score(db)
    query_8_grade_distribution(db)
    query_9_top_10_students(db)

    print("\nAll queries completed. No data was modified.")