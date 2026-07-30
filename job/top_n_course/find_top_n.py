import os
import sys

TOP_N = 10


def read_part_file(filepath, results):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            parts = line.split("\t")

            if len(parts) != 2:
                continue

            course_id, count = parts

            try:
                count = int(count)
            except ValueError:
                continue

            results.append((course_id, count))


def main():

    if len(sys.argv) != 3:
        print(
            "Usage: python find_top_n.py <count_course_output_folder> <output_file>"
        )
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    results = []

    for filename in os.listdir(input_folder):

        if filename.startswith("part-"):

            filepath = os.path.join(input_folder, filename)

            read_part_file(filepath, results)

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    with open(output_file, "w", encoding="utf-8") as f:

        for course_id, count in results[:TOP_N]:

            f.write(f"{course_id}\t{count}\n")


if __name__ == "__main__":
    main()