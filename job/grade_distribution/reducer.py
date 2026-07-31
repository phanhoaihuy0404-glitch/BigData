import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():

    current_grade = None
    count = 0

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        grade, value = line.split("\t", 1)
        value = int(value)

        if current_grade == grade:
            count += value
        else:

            if current_grade is not None:
                emit(current_grade, count)

            current_grade = grade
            count = value

    if current_grade is not None:
        emit(current_grade, count)


if __name__ == "__main__":
    main()