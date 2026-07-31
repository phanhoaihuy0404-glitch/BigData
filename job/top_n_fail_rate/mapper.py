import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) != 3:
            continue

        course_id = parts[0]

        try:
            total_pass = int(parts[1])
            total_fail = int(parts[2])
        except ValueError:
            continue

        total = total_pass + total_fail

        if total == 0:
            continue

        fail_rate = (total_fail / total) * 100

        emit("ALL", f"{course_id}\t{fail_rate:.2f}")


if __name__ == "__main__":
    main()