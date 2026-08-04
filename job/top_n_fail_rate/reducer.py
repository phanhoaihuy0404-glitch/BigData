import sys


DEFAULT_TOP_N = 10


def emit(course_id, fail_rate):
    print(f"{course_id}\t{fail_rate:.2f}")


def main():

    top_n = DEFAULT_TOP_N

    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
            if top_n <= 0:
                top_n = DEFAULT_TOP_N
        except ValueError:
            top_n = DEFAULT_TOP_N

    records = []

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) == 3 and parts[0] == "ALL":
            course_id = parts[1]
            fail_rate = parts[2]
        elif len(parts) == 2:
            course_id = parts[0]
            fail_rate = parts[1]
        else:
            continue

        try:
            fail_rate = float(fail_rate)
        except ValueError:
            continue

        records.append((course_id, fail_rate))

    records.sort(key=lambda x: x[1], reverse=True)

    for course_id, fail_rate in records[:top_n]:
        emit(course_id, fail_rate)


if __name__ == "__main__":
    main()