"""
Wrapper module that provides the EnrollmentParser class interface
by delegating to the new csv_parser module.
"""

import sys
import os

# Add the new parser directory to sys.path
_new_parser_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "parser (1)")
if _new_parser_dir not in sys.path:
    sys.path.insert(0, _new_parser_dir)

from csv_parser import parse_enrollment


class EnrollmentParser:
    """
    Provides a parse() static method that delegates to csv_parser.parse_enrollment().

    Usage:
        from parser.enrollment_parser import EnrollmentParser
        record = EnrollmentParser.parse(line)
    """

    @staticmethod
    def parse(line: str):
        return parse_enrollment(line)

