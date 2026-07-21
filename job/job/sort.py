#!/usr/bin/env python3
"""
sort.py - Drop-in replacement for Windows sort.exe that uses Python's sort.

Usage: type input.txt | python sort.py > output.txt

This script reads all lines from stdin, sorts them, and writes to stdout.
It handles Windows memory limitations that cause native sort.exe to fail.
"""
import sys


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line)

    lines.sort()

    sys.stdout.writelines(lines)


if __name__ == "__main__":
    main()

