import sys

TOP_N = 10

def emit(course_id, count):
    print(f"{course_id}\t{count}")


def main():

    courses = []

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        #<"CourseID": TotalScore \t StudentCount> 
        key, value = line.split("\t", 1)


        parts = value.split("\t")

        if len(parts) != 2:
            continue

        course_id, count = parts

        try:
            count = int(count)
        except ValueError:
            continue

        courses.append((course_id, count))

    courses.sort(key=get_count, reverse=True)

    for course_id, count in courses[:TOP_N]:
        emit(course_id, count)

def get_count(course):
    return course[1]

if __name__ == "__main__":
    main()