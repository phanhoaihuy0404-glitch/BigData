import sys

def emit(key, value):
    print(f"{key}\t{value}")


def main():

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) != 2:
            continue

        course_id, count = parts

        emit("TopN", f"{course_id}\t{count}")


if __name__ == "__main__":
    main()