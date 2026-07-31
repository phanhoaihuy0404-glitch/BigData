import sys
import os

# Add project root
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from csv_parser import parse_student, parse_enrollment


def emit(key, value):
    print(f"{key}\t{value}")


def emit_student(student):

    emit(
        # StudentID    Collection_Flag|LastName|FirstName
        student["StudentID"],f"Students|{student['LastName']}|{student['FirstName']}"
    )


def emit_enrollment(enrollment):
    # StudentID    Collection_Flag|CourseID|TotalScore
    emit(
        enrollment["StudentID"], f"Enrollments|{enrollment['CourseID']}|{enrollment['TotalScore']}"
    )





def map_student(line):

    student = parse_student(line)

    if student is None:
        return

    emit_student(student)


def map_enrollment(line):

    enrollment = parse_enrollment(line)

    if enrollment is None:
        return

    emit_enrollment(enrollment)




def main():

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        columns = line.split(",")

        #VÌ Student.csv có 5 cột, Enrollment.csv có 9 cột nên dùng số cột để phân biệt đơn giản hơn so với dùng tên file
        # Student.csv
        if len(columns) == 5 and columns[0].lower() != "studentid":
            map_student(line)

        # Enrollment.csv
        elif len(columns) == 9 and columns[0].lower() != "enrollmentid":
            map_enrollment(line)
        

if __name__ == "__main__":
    main()