import sys


def emit(course_id, passed, failed):
    print(f"{course_id}\t{passed}\t{failed}")


def main():

    current_course = None

    pass_count = 0
    fail_count = 0

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        course_id, status = line.split("\t")

        if current_course is None:

            current_course = course_id

            if status == "PASS":
                pass_count = 1
                fail_count = 0
            else:
                pass_count = 0
                fail_count = 1

        elif course_id == current_course:

            if status == "PASS":
                pass_count += 1
            else:
                fail_count += 1

        else:

            emit(current_course, pass_count, fail_count)

            current_course = course_id

            if status == "PASS":
                pass_count = 1
                fail_count = 0
            else:
                pass_count = 0
                fail_count = 1

    if current_course is not None:
        emit(current_course, pass_count, fail_count)


if __name__ == "__main__":
    main()