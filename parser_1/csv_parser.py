from typing import Optional

EXPECTED_ENROLLMENT_COLUMNS = 9
EXPECTED_STUDENT_COLUMNS = 5
EXPECTED_COURSE_COLUMNS = 3


def parse_enrollment(line: str) -> Optional[dict]:

    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_ENROLLMENT_COLUMNS:
        return None

    return {
        "EnrollmentID": int(columns[0]),
        "StudentID": int(columns[1]),
        "CourseID": columns[2],
        "Semester": columns[3],
        "Year": int(columns[4]),
        "MidtermScore": float(columns[5]),
        "FinalScore": float(columns[6]),
        "TotalScore": float(columns[7]),
        "LetterGrade": columns[8]
    }


def parse_student(line: str) -> Optional[dict]:


    line = line.strip()

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
        "DateOfBirth": columns[4]
    }


def parse_course(line: str) -> Optional[dict]:
    """
    Convert one Course CSV line into a dictionary.

    Returns:
        dict if parsing succeeds.
        None if the line is invalid.
    """

    line = line.strip()

    if not line:
        return None

    columns = line.split(",")

    if len(columns) != EXPECTED_COURSE_COLUMNS:
        return None

    return {
        "CourseID": columns[0],
        "CourseName": columns[1],
        "Credits": int(columns[2])
    }