import sys


def emit(course_id, students, score):
    print(f"{course_id}\t{','.join(students)}\t{score}")


def main():
    current_course = None
    max_score = float("-inf")
    current_students = []

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) != 2:
            continue

        course_id, value = parts

        try:
            student_id, score_str = value.split(",")
            score = float(score_str)
        except ValueError:
            continue

        # First record
        if current_course is None:
            current_course = course_id
            max_score = score
            current_students = [student_id]

        # Same course
        elif course_id == current_course:

            if score > max_score:
                max_score = score
                current_students = [student_id]

            elif score == max_score:
                current_students.append(student_id)

        # Different course
        else:
            emit(current_course, current_students, max_score)

            current_course = course_id
            max_score = score
            current_students = [student_id]

    # Last course
    if current_course is not None:
        emit(current_course, current_students, max_score)


if __name__ == "__main__":
    main()