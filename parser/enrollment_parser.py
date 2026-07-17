from typing import Optional

class EnrollmentParser:
    """
    Parse one line from Enrollment.csv
    """

    EXPECTED_COLUMNS = 9

    @staticmethod
    def parse(line: str) -> Optional[dict]:
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

        if len(columns) != EnrollmentParser.EXPECTED_COLUMNS:
            return None

        try:
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

        except ValueError:
            return None