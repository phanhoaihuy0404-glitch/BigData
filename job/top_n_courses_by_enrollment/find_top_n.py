import sys



DEFAULT_TOP_N = 10


def emit(course_id, count):
    print(f"{course_id}\t{count}")


def get_count(course):
    return course[1]


def main(top_n):

    courses = []

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        # Input: CourseID<TAB>Count
        try:
            course_id, count = line.split("\t")
            count = int(count)
        except ValueError:
            continue

        courses.append((course_id, count))

    courses.sort(key=get_count, reverse=True)

    for course_id, count in courses[:top_n]:
        emit(course_id, count)


if __name__ == "__main__":

    top_n = DEFAULT_TOP_N
    #sys.argv[0] is name, sys.argv[1] is first argument
    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])

            if top_n <= 0:
                top_n = DEFAULT_TOP_N

        except ValueError:
            top_n = DEFAULT_TOP_N

    main(top_n)