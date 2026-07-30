import random
from datetime import datetime, timedelta

import pandas as pd

from config import *

# ===============================
# Name Lists
# ===============================

FIRST_NAMES = [
    "An", "Anh", "Bao", "Bach", "Binh", "Chau", "Chi", "Cong", "Cuong",
    "Dan", "Dao", "Dat", "Diep", "Diem", "Dinh", "Dung", "Duong",
    "Giang", "Ha", "Hai", "Han", "Hanh", "Hao", "Hiep", "Hieu", "Hoa",
    "Hoai", "Hong", "Hung", "Huong", "Huy", "Khanh", "Khang", "Khiet",
    "Khoa", "Kien", "Kim", "Lam", "Lan", "Le", "Lien", "Linh", "Loan",
    "Loc", "Long", "Luan", "Luan", "Ly", "Mai", "Manh", "Minh", "My",
    "Nam", "Nga", "Ngan", "Ngoc", "Nghi", "Nghia", "Nhi", "Nhan",
    "Nhat", "Nhu", "Nhuan", "Nhuy", "Ninh", "Nu", "Oanh", "Phat",
    "Phi", "Phong", "Phu", "Phuc", "Phung", "Phuong", "Quan", "Quang",
    "Quoc", "Quyen", "Quynh", "Sang", "Son", "Sy", "Tam", "Tan",
    "Tay", "Thai", "Thanh", "Thao", "Thien", "Thinh", "Thong", "Thu",
    "Thuan", "Thuc", "Thuy", "Tien", "Tin", "Toan", "Trang", "Tri",
    "Trinh", "Truc", "Trung", "Tuan", "Tung", "Tuyet", "Uyen", "Van",
    "Vi", "Viet", "Vinh", "Vy", "Xuan", "Yen", "Y", "Ynh",
    "Ai", "Bao Chau", "Bao Ngoc", "Cam"
]

LAST_NAMES = [
    "Nguyen",
    "Tran",
    "Le",
    "Pham",
    "Hoang",
    "Vo",
    "Dang",
    "Do",
    "Bui",
    "Ngo",
    "Duong",
    "Ly"
]

# ===============================
# Birthday Range
# ===============================

START_DATE = datetime(2006, 1, 1)
END_DATE = datetime(2007, 12, 31)

TOTAL_DAYS = (END_DATE - START_DATE).days

# ===============================
# Generate Students
# ===============================

students = []

for i in range(1, NUM_STUDENTS + 1):

    birthday = START_DATE + timedelta(
        days=random.randint(0, TOTAL_DAYS)
    )

    student = {

        "StudentID": 2500000 + i,

        "FirstName": random.choice(FIRST_NAMES),

        "LastName": random.choice(LAST_NAMES),

        "Gender": random.choice([
            "Male",
            "Female"
        ]),

        "DateOfBirth": birthday.strftime("%Y-%m-%d")

    }

    students.append(student)

# ===============================
# Save CSV
# ===============================

df = pd.DataFrame(students)

output_file = DATA_FOLDER / "Student.csv"

df.to_csv(
    output_file,
    index=False
)

print("=" * 50)
print("Student Dataset Generated")
print("=" * 50)
print(f"Total Students : {len(df)}")
print(f"Output File    : {output_file}")