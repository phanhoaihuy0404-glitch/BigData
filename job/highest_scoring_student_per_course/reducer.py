import sys

def main():
    current_course = None
    current_students = []
    max_score = float("-inf")

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            course_id, student_id, score_str = raw.split("\t")
        except ValueError:
            continue

        try:
            score = float(score_str)
        except (ValueError, TypeError):
            continue

        # First Record ^^
        if current_course is None:
            current_course = course_id
            current_students = [student_id]
            max_score = score
            continue

        # Different Course..
        if course_id != current_course:
            sys.stdout.write(
                f"{current_course}\t{','.join(current_students)}\t{max_score}\n"
            )

            current_course = course_id
            current_students = [student_id]
            max_score = score

        # Same Course
        else:
            if score > max_score:
                max_score = score
                current_students = [student_id]

            elif score == max_score:
                current_students.append(student_id)

    # Output Course cuối cùng
    if current_course is not None:
        sys.stdout.write(
            f"{current_course}\t{','.join(current_students)}\t{max_score}\n"
        )


if __name__ == "__main__":
    main()