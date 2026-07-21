#!/usr/bin/env python3
"""
Reducer for Course performance analytics (multi-metrics).

Input : course_id<TAB>total_score,1,pass_flag,letter_grade
Output: course_id<TAB>AVG_TOTAL:<avg>,PASS_RATE:<rate>,GRADES:<A:count,B:count,...>
"""

import sys


def format_grades(grades_dict: dict) -> str:
    letters = sorted(grades_dict.keys())
    return ",".join([f"{l}:{grades_dict[l]}" for l in letters])


def main():
    current_course = None

    total_score_sum = 0.0
    total_students = 0
    pass_count = 0
    grade_counts = {}

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue

        try:
            course_id, payload = raw.split("\t", 1)
        except ValueError:
            continue

        # payload: total_score,1,pass_flag,letter_grade
        try:
            score_str, one_str, pass_str, letter_grade = payload.split(",", 3)
        except ValueError:
            continue

        try:
            total_score = float(score_str)
            cnt = int(one_str)
            pass_flag = int(pass_str)
        except (ValueError, TypeError):
            continue

        if current_course is None:
            current_course = course_id

        if course_id != current_course:
            avg_total = (total_score_sum / total_students) if total_students > 0 else 0.0
            pass_rate = (pass_count / total_students) if total_students > 0 else 0.0
            grades_part = format_grades(grade_counts)

            sys.stdout.write(
                f"{current_course}\tAVG_TOTAL:{avg_total:.2f},PASS_RATE:{pass_rate:.2%},GRADES:{grades_part}\n"
            )

            # reset
            current_course = course_id
            total_score_sum = 0.0
            total_students = 0
            pass_count = 0
            grade_counts = {}

        total_score_sum += total_score * cnt
        total_students += cnt
        if pass_flag == 1:
            pass_count += cnt

        grade = letter_grade.strip()
        if grade:
            grade_counts[grade] = grade_counts.get(grade, 0) + cnt

    if current_course is not None:
        avg_total = (total_score_sum / total_students) if total_students > 0 else 0.0
        pass_rate = (pass_count / total_students) if total_students > 0 else 0.0
        grades_part = format_grades(grade_counts)

        sys.stdout.write(
            f"{current_course}\tAVG_TOTAL:{avg_total:.2f},PASS_RATE:{pass_rate:.2%},GRADES:{grades_part}\n"
        )


if __name__ == "__main__":
    main()

