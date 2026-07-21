from typing import Optional

EXPECTED_ENROLLMENT_COLUMNS = 9
EXPECTED_STUDENT_COLUMNS = 6
EXPECTED_TEACHER_COLUMNS = 4
EXPECTED_COURSE_COLUMNS = 5
EXPECTED_CLASS_COLUMNS = 3
EXPECTED_DEPARTMENT_COLUMNS = 2


def parse_enrollment(line: str) -> Optional[dict]:
    """
    Convert one CSV line into a dictionary.

    Returns:
        dict if parsing succeeds.
        None if the line is invalid.
    """

    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_ENROLLMENT_COLUMNS:
        return None

    return {
        "enrollment_id": int(columns[0]),
        "student_id": int(columns[1]),
        "course_id": columns[2],
        "semester": columns[3],
        "year": int(columns[4]),
        "midterm_score": float(columns[5]),
        "final_score": float(columns[6]),
        "total_score": float(columns[7]),
        "letter_grade": columns[8]
    }


def parse_student(line: str) -> Optional[dict]:

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_STUDENT_COLUMNS:
        return None

    return {
        "StudentID": int(columns[0]),
        "FirstName": columns[1],
        "LastName": columns[2],
        "Gender": columns[3],
        "DateOfBirth": columns[4],
        "ClassID": columns[5]
    }


def parse_teacher(line: str) -> Optional[dict]:
    line = line.strip()

    if not line:
        return None 

    columns = line.split(",")

    if len(columns) != EXPECTED_TEACHER_COLUMNS:
        return None

    return {
        "TeacherID": columns[0],
        "TeacherName": columns[1],
        "Email": columns[2],
        "Phone": columns[3]
    }


def parse_course(line: str) -> Optional[dict]:

    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_COURSE_COLUMNS:
        return None

    return {
        "CourseID": columns[0],
        "CourseName": columns[1],
        "DepartmentID": columns[2],
        "Credits": int(columns[3]),
        "TeacherID": columns[4]
    }


def parse_class(line: str) -> Optional[dict]:

    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_CLASS_COLUMNS:
        return None

    return {
        "ClassID": columns[0],
        "ClassName": columns[1],
        "DepartmentID": columns[2]
    }


def parse_department(line: str) -> Optional[dict]:
 
    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_DEPARTMENT_COLUMNS:
        return None

    return {
        "DepartmentID": columns[0],
        "DepartmentName": columns[1]
    }