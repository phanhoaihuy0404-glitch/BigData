import sys


def emit(key, value):
    print(f"{key}\t{value}")


def main():

    current_key = None
    current_count = 0

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        key, value = line.split("\t")

        value = int(value)

        if current_key is None:

            current_key = key
            current_count = value

        elif key == current_key:

            current_count += value

        else:

            emit(current_key, current_count)

            current_key = key
            current_count = value

    if current_key is not None:
        emit(current_key, current_count)


if __name__ == "__main__":
    main()