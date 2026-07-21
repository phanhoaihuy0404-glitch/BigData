#!/usr/bin/env python3
"""
Post-processing script: Find Top N courses with the highest enrollment counts.

Input : A file where each line is "CourseID<TAB>Count" (output from top_n_course reducer)
Output: Top N courses sorted by count descending.

Usage:
    python3 job/top_n_course/find_top_n.py <input_file> [N]

Examples:
    python3 job/top_n_course/find_top_n.py data/output/top_n_course.txt 5
    python3 job/top_n_course/find_top_n.py data/output/top_n_course.txt 10
"""

import sys


def main():
    # Determine N from command-line args
    if len(sys.argv) >= 2 and sys.argv[1] != "-":
        input_path = sys.argv[1]
        infile = open(input_path, "r")
    else:
        infile = sys.stdin

    n = 10  # default
    if len(sys.argv) >= 3:
        try:
            n = int(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid N value '{sys.argv[2]}', using default 10", file=sys.stderr)

    counts: dict[str, int] = {}

    for line in infile:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        course_id, count_str = parts
        try:
            counts[course_id] = int(count_str)
        except ValueError:
            continue

    if infile is not sys.stdin:
        infile.close()

    # Sort by count descending, then by course_id ascending for tie-breaking
    sorted_courses = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    # Output header
    print(f"{'Rank':<6}{'CourseID':<15}{'Enrollments':<12}")
    print("-" * 33)

    for rank, (course_id, count) in enumerate(sorted_courses[:n], start=1):
        print(f"{rank:<6}{course_id:<15}{count:<12}")


if __name__ == "__main__":
    main()

