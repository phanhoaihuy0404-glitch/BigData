import sys


def emit(key, value):
    print(f"{key}\t{value:.2f}")


def main():

    current_key = None
    score_sum = 0
    score_count = 0

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        key, value = line.split("\t")

        try:
            value = float(value)
        except ValueError:
            continue

        if current_key is None:

            current_key = key
            score_sum = value
            score_count = 1

        elif key == current_key:

            score_sum += value
            score_count += 1

        else:

            average = score_sum / score_count

            emit(current_key, average)

            current_key = key
            score_sum = value
            score_count = 1

    if current_key is not None:

        average = score_sum / score_count

        emit(current_key, average)


if __name__ == "__main__":
    main()