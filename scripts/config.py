import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent

files = [
    "generate_students.py",
    "generate_courses.py",
    "generate_enrollments.py"
]

print()

# Generate CSV files
for file in files:

    print("=" * 60)
    print(file)
    print("=" * 60)

    subprocess.run(
        [sys.executable, ROOT / file],
        check=True,
        cwd=PROJECT_ROOT
    )

# Import into MongoDB
print()
print("=" * 60)
print("Importing data into MongoDB...")
print("=" * 60)

subprocess.run(
    [sys.executable, "-m", "mongodb.import_data"],
    check=True,
    cwd=PROJECT_ROOT
)

print()
print("=" * 60)
print("ALL DATASETS GENERATED AND IMPORTED SUCCESSFULLY")
print("=" * 60)