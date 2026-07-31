#!/usr/bin/env python3
import sys


DEFAULT_COURSE_ID = "251AI1"
DEFAULT_START_SCORE = 0
DEFAULT_END_SCORE = 100


def emit(student_id, last_name, first_name):
    print(f"{student_id}\t{last_name}\t{first_name}")


def process_student(student_id, values, course_id, start_score, end_score):

    last_name = None
    first_name = None

    enrollments = []


    # Separate Student and Enrollment records
    for value in values:

        parts = value.split("|")

        if parts[0] == "Students":

            last_name = parts[1]
            first_name = parts[2]


        elif parts[0] == "Enrollments":

            enroll_course = parts[1]
            total_score = float(parts[2])

            enrollments.append(
                (enroll_course, total_score)
            )


    # Join + Filter
    if last_name is None or first_name is None:
        return


    for enroll_course, total_score in enrollments:

        if enroll_course == course_id:

            if start_score <= total_score <= end_score:

                emit(
                    student_id,
                    last_name,
                    first_name
                )


def main():

    # Default parameter
    course_id = DEFAULT_COURSE_ID
    start_score = DEFAULT_START_SCORE
    end_score = DEFAULT_END_SCORE


    # Read parameters from command line
    if len(sys.argv) > 1:
        course_id = sys.argv[1]

    if len(sys.argv) > 2:
        start_score = float(sys.argv[2])

    if len(sys.argv) > 3:
        end_score = float(sys.argv[3])


    current_student_id = None
    values = []


    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue


        student_id, value = line.split("\t", 1)


        # Same StudentID
        if current_student_id == student_id:

            values.append(value)


        else:

            # Process previous StudentID
            if current_student_id is not None:

                process_student(
                    current_student_id,
                    values,
                    course_id,
                    start_score,
                    end_score
                )


            current_student_id = student_id
            values = [value]


    # Process last StudentID
    if current_student_id is not None:

        process_student(
            current_student_id,
            values,
            course_id,
            start_score,
            end_score
        )


if __name__ == "__main__":
    main()