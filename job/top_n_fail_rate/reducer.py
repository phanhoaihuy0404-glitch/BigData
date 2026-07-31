import sys


def emit(course_id, fail_rate):
    print(f"{course_id}\t{fail_rate:.2f}")


def main():

    records = []

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) != 3:
            continue

        try:
            fail_rate = float(parts[2])
        except ValueError:
            continue

        course_id = parts[1]

        records.append((course_id, fail_rate))

    records.sort(key=lambda x: x[1], reverse=True)

    for course_id, fail_rate in records:

        emit(course_id, fail_rate)


if __name__ == "__main__":
    main()