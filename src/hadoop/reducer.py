#!/usr/bin/env python3

import sys


def main():

    current_course = None
    total = 0

    for line in sys.stdin:

        line = line.strip()

        if not line:
            continue

        course_id, value = line.split('\t')

        value = int(value)


        if current_course == course_id:

            total += value

        else:

            if current_course is not None:
                print(f"{current_course}\t{total}")

            current_course = course_id
            total = value


    if current_course is not None:
        print(f"{current_course}\t{total}")


if __name__ == "__main__":
    main()