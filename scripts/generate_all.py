import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

files = [
    "generate_students.py",
    "generate_courses.py",
    "generate_enrollments.py"
]

print()

for file in files:

    print("=" * 60)
    print(file)
    print("=" * 60)

    subprocess.run(
        [sys.executable, ROOT / file],
        check=True
    )

print()
print("=" * 60)
print("ALL DATASETS GENERATED SUCCESSFULLY")
print("=" * 60)