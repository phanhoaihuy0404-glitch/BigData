# Big Data University Project — MongoDB Schema Redesign

## 1. Current Schema Analysis

### Existing Collections (from CSV files)

| Collection | Fields |
|---|---|
| **students** | StudentID, FirstName, LastName, Gender, DateOfBirth, Major, GPA |
| **courses** | CourseID, CourseName, Department, Credits, Instructor |
| **enrollments** | EnrollmentID, StudentID, CourseID, Semester, Year, Grade |
| **grades** | GradeID, StudentID, CourseID, AssignmentType, Score, Date |
| **attendance** | AttendanceID, StudentID, CourseID, Date, AttendanceStatus |
| **feedback** | FeedbackID, StudentID, FeedbackDate, FeedbackText |

---

## 2. Problems with the Current Design

### Problem 1: No Department Collection
- **Current state:** `Department` is stored as a plain string in `courses.csv` (e.g., "Mathematics", "Physics", "Computer Science", "Biology").
- **Why it's a problem:** This is denormalized data. If a department name changes, every course record must be updated. There is no place to store department-level metadata (e.g., department head, office location, budget).
- **Real university logic:** Every real university has a Department entity that organizes classes, courses, and teachers.

### Problem 2: No Class Collection
- **Current state:** Students have no `ClassID`. The `Major` field in `students.csv` is a string that loosely groups students by field of study.
- **Why it's a problem:** In real universities, students are organized into **classes** (e.g., "CS2024A", "PHY2023B"). A class has a specific academic year, a homeroom teacher, and belongs to a department. Without this, we cannot answer questions like "Which students are in the same class?" or "What is the class composition for a given year?"
- **Real university logic:** A student belongs to exactly one class. A class belongs to exactly one department.

### Problem 3: No Teacher Collection
- **Current state:** `Instructor` is stored as a plain string in `courses.csv` (e.g., "Instructor 1", "Instructor 2").
- **Why it's a problem:** Same denormalization issue as Department. No place for teacher metadata (specialization, hire date, contact info). A teacher can teach multiple courses, but there is no single source of truth for teacher identity.
- **Real university logic:** Teachers are independent entities with their own attributes. Courses reference teachers, not the other way around.

### Problem 4: Grades Collection is Fragmented and Unrealistic
- **Current state:** `grades.csv` stores individual assignment scores as separate rows with `AssignmentType` (Midterm, Quiz, Assignment, Final Exam). A single enrollment can have 4+ grade rows.
- **Why it's a problem:**
  - This is not how real university grading works. A student receives one **MidtermScore**, one **FinalScore**, a computed **TotalScore**, and a **LetterGrade** per course enrollment.
  - The current design makes it extremely difficult to compute final grades. You must aggregate multiple rows per student-course pair.
  - The `grades.csv` data is inconsistent with `enrollments.csv` — the analysis script already shows mismatches between enrollment pairs and grade pairs.
- **Real university logic:** Each enrollment has a fixed set of score fields (Midterm, Final, Total, LetterGrade). Individual assignment scores are internal teacher records, not part of the official academic record.

### Problem 5: Enrollment Has Only a Letter Grade
- **Current state:** `enrollments.csv` has only a `Grade` column (A, B, C, D, F).
- **Why it's a problem:** There is no way to know the numerical scores that produced the letter grade. This makes GPA calculation, academic analytics, and performance trend analysis impossible.
- **Real university logic:** Enrollments store both numerical scores and the derived letter grade.

### Problem 6: Feedback Collection is Out of Scope
- **Current state:** `feedback.csv` stores student feedback text with a date.
- **Why it's a problem:** Feedback is not core to the academic data model. It adds complexity without contributing to the primary project goals (enrollment, grading, attendance tracking). It can be added later as a separate module if needed.
- **Real university logic:** Feedback is typically a separate system, not part of the core academic database.

---

## 3. Proposed Schema Redesign

### Final Collections (7 total)

1. **Department**
2. **Class**
3. **Student**
4. **Teacher**
5. **Course**
6. **Enrollment**
7. **Attendance**

---

### 3.1 Department Collection

**Purpose:** Normalize department data. Each department has a unique ID, name, and optional metadata.

```json
{
  "_id": "DEPT001",
  "DepartmentName": "Computer Science",
  "Description": "Study of computation and information processing"
}
```

**Why this change is necessary:**
- Eliminates string duplication across courses.
- Provides a single source of truth for department data.
- Enables department-level analytics (e.g., "How many students per department?").

**Impact on the project:**
- `Course` will reference `DepartmentID` instead of storing a string.
- `Class` will reference `DepartmentID`.
- ETL must create Department documents from unique department values in courses.csv.

---

### 3.2 Class Collection

**Purpose:** Represent a real university class (e.g., "CS2024A"). A class groups students by academic year and department.

```json
{
  "_id": "CLASS001",
  "ClassName": "CS2024A",
  "DepartmentID": "DEPT001",
  "AcademicYear": 2024,
  "Section": "A"
}
```

**Why this change is necessary:**
- Real universities organize students into classes.
- Enables queries like "List all students in class CS2024A."
- Provides a bridge between Student and Department.

**Impact on the project:**
- `Student` will gain a `ClassID` field.
- `Class` belongs to one `Department`.
- ETL must generate class data (this is synthetic data not present in the original CSV).

---

### 3.3 Student Collection

**Purpose:** Store student personal and academic information. Now linked to a Class.

```json
{
  "_id": "STU1001",
  "FirstName": "Student1",
  "LastName": "Doe",
  "Gender": "Female",
  "DateOfBirth": "2004-09-03",
  "ClassID": "CLASS001",
  "GPA": 2.33
}
```

**Changes from current:**
- **Removed:** `Major` (replaced by Class → Department relationship).
- **Added:** `ClassID` (reference to Class collection).

**Why this change is necessary:**
- A student's major/department is now derived from their class, not stored redundantly.
- The ClassID creates a proper hierarchical structure: Department → Class → Student.

**Impact on the project:**
- Queries for "students in a department" now go through Class.
- ETL must assign each student to a class based on their Major field.

---

### 3.4 Teacher Collection

**Purpose:** Normalize teacher data. Teachers are independent entities.

```json
{
  "_id": "TCH001",
  "FirstName": "John",
  "LastName": "Smith",
  "Email": "john.smith@university.edu",
  "Specialization": "Computer Science",
  "DepartmentID": "DEPT001"
}
```

**Why this change is necessary:**
- Eliminates string duplication of instructor names in courses.
- Provides a single source of truth for teacher data.
- Enables teacher-level analytics (course load, student performance by teacher).

**Impact on the project:**
- `Course` will reference `TeacherID` instead of storing `Instructor` string.
- ETL must create Teacher documents from unique instructor values in courses.csv.

---

### 3.5 Course Collection

**Purpose:** Store course information with proper references.

```json
{
  "_id": "COURSE1",
  "CourseName": "Course 1",
  "DepartmentID": "DEPT003",
  "Credits": 2,
  "TeacherID": "TCH001"
}
```

**Changes from current:**
- **Removed:** `Department` (string) → replaced by `DepartmentID` (reference).
- **Removed:** `Instructor` (string) → replaced by `TeacherID` (reference).

**Why this change is necessary:**
- Proper normalization. Course now references both Department and Teacher.
- Enables join queries: "Which teacher teaches which course in which department?"

**Impact on the project:**
- All course queries must now use references instead of string lookups.
- ETL must map Department strings to DepartmentIDs and Instructor strings to TeacherIDs.

---

### 3.6 Enrollment Collection

**Purpose:** Record a student's enrollment in a course with full grading information.

```json
{
  "_id": "ENR001",
  "StudentID": "STU1001",
  "CourseID": "COURSE1",
  "Semester": "Fall",
  "Year": 2024,
  "MidtermScore": 85,
  "FinalScore": 90,
  "TotalScore": 87.5,
  "LetterGrade": "B+"
}
```

**Changes from current:**
- **Removed:** `Grade` (single letter) → replaced by structured scoring.
- **Added:** `MidtermScore`, `FinalScore`, `TotalScore`, `LetterGrade`.

**Why this change is necessary:**
- The old `Grade` field was insufficient for analytics.
- The separate `grades` collection was fragmented and unrealistic.
- Now all grade information for an enrollment is in one document.
- `TotalScore` can be computed as a weighted average of Midterm and Final.
- `LetterGrade` is derived from `TotalScore` using a standard scale.

**Impact on the project:**
- The old `grades` collection is completely removed.
- ETL must aggregate the old grades.csv data per student-course pair to compute MidtermScore, FinalScore, TotalScore, and LetterGrade.
- This simplifies all grade-related queries to a single collection lookup.

---

### 3.7 Attendance Collection

**Purpose:** Track student attendance per course session. **Unchanged** from the original design.

```json
{
  "_id": "ATT001",
  "StudentID": "STU1001",
  "CourseID": "COURSE1",
  "Date": "2024-09-15",
  "AttendanceStatus": "Present"
}
```

**Why this stays the same:**
- The attendance schema is already well-designed for a university project.
- It tracks individual session attendance per student per course.

---

## 4. Entity Relationship Diagram (ERD)

```
┌──────────────────┐       ┌──────────────────┐
│    Department    │       │     Teacher      │
├──────────────────┤       ├──────────────────┤
│ PK DepartmentID  │       │ PK TeacherID     │
│ DepartmentName   │       │ FirstName        │
│ Description      │       │ LastName         │
└────────┬─────────┘       │ Email            │
         │                 │ Specialization   │
         │                 │ DepartmentID(FK) │
         │                 └────────┬─────────┘
         │                          │
         │ 1                        │ 1
         │                          │
         ▼                          ▼
┌──────────────────┐       ┌──────────────────┐
│      Class       │       │      Course      │
├──────────────────┤       ├──────────────────┤
│ PK ClassID       │       │ PK CourseID      │
│ ClassName        │       │ CourseName       │
│ DepartmentID(FK) │       │ DepartmentID(FK) │
│ AcademicYear     │       │ Credits          │
│ Section          │       │ TeacherID(FK)    │
└────────┬─────────┘       └────────┬─────────┘
         │                          │
         │ 1                        │ M
         │                          │
         ▼                          ▼
┌──────────────────┐       ┌──────────────────┐
│     Student      │       │   Enrollment     │
├──────────────────┤       ├──────────────────┤
│ PK StudentID     │       │ PK EnrollmentID  │
│ FirstName        │       │ StudentID(FK)    │
│ LastName         │       │ CourseID(FK)     │
│ Gender           │       │ Semester         │
│ DateOfBirth      │       │ Year             │
│ ClassID(FK)      │       │ MidtermScore     │
│ GPA              │       │ FinalScore       │
└────────┬─────────┘       │ TotalScore       │
         │                 │ LetterGrade      │
         │                 └──────────────────┘
         │
         │
         ▼
┌──────────────────┐
│   Attendance     │
├──────────────────┤
│ PK AttendanceID  │
│ StudentID(FK)    │
│ CourseID(FK)     │
│ Date             │
│ AttendanceStatus │
└──────────────────┘
```

### Relationship Summary

| Relationship | Type | Description |
|---|---|---|
| Department → Class | 1 : M | One department has many classes |
| Department → Course | 1 : M | One department offers many courses |
| Department → Teacher | 1 : M | One department employs many teachers |
| Class → Student | 1 : M | One class contains many students |
| Course → Teacher | M : 1 | Many courses are taught by one teacher |
| Student → Enrollment | 1 : M | One student has many enrollments |
| Course → Enrollment | 1 : M | One course has many enrollments |
| Student → Attendance | 1 : M | One student has many attendance records |
| Course → Attendance | 1 : M | One course has many attendance records |

---

## 5. Collection Definitions (MongoDB)

### Department
```json
{
  "_id": "string (PK)",
  "DepartmentName": "string",
  "Description": "string (optional)"
}
```

### Class
```json
{
  "_id": "string (PK)",
  "ClassName": "string",
  "DepartmentID": "string (FK → Department)",
  "AcademicYear": "int",
  "Section": "string"
}
```

### Student
```json
{
  "_id": "string (PK)",
  "FirstName": "string",
  "LastName": "string",
  "Gender": "string",
  "DateOfBirth": "date",
  "ClassID": "string (FK → Class)",
  "GPA": "double"
}
```

### Teacher
```json
{
  "_id": "string (PK)",
  "FirstName": "string",
  "LastName": "string",
  "Email": "string",
  "Specialization": "string",
  "DepartmentID": "string (FK → Department)"
}
```

### Course
```json
{
  "_id": "string (PK)",
  "CourseName": "string",
  "DepartmentID": "string (FK → Department)",
  "Credits": "int",
  "TeacherID": "string (FK → Teacher)"
}
```

### Enrollment
```json
{
  "_id": "string (PK)",
  "StudentID": "string (FK → Student)",
  "CourseID": "string (FK → Course)",
  "Semester": "string (enum: Spring, Summer, Fall)",
  "Year": "int",
  "MidtermScore": "double (nullable)",
  "FinalScore": "double (nullable)",
  "TotalScore": "double (nullable)",
  "LetterGrade": "string (nullable)"
}
```

### Attendance
```json
{
  "_id": "string (PK)",
  "StudentID": "string (FK → Student)",
  "CourseID": "string (FK → Course)",
  "Date": "date",
  "AttendanceStatus": "string (enum: Present, Absent)"
}
```

---

## 6. Suggested Indexes

### Department
- `{ DepartmentName: 1 }` — unique index for fast lookup by name

### Class
- `{ ClassName: 1 }` — unique index
- `{ DepartmentID: 1 }` — for queries filtering classes by department

### Student
- `{ ClassID: 1 }` — for queries filtering students by class
- `{ LastName: 1, FirstName: 1 }` — for name-based searches

### Teacher
- `{ DepartmentID: 1 }` — for queries filtering teachers by department
- `{ Email: 1 }` — unique index

### Course
- `{ DepartmentID: 1 }` — for queries filtering courses by department
- `{ TeacherID: 1 }` — for queries filtering courses by teacher
- `{ CourseName: 1 }` — for name-based searches

### Enrollment
- `{ StudentID: 1, CourseID: 1 }` — **compound unique index** to prevent duplicate enrollments
- `{ StudentID: 1, Year: 1, Semester: 1 }` — for student semester transcripts
- `{ CourseID: 1, Year: 1, Semester: 1 }` — for course enrollment reports
- `{ LetterGrade: 1 }` — for grade distribution analysis

### Attendance
- `{ StudentID: 1, CourseID: 1, Date: 1 }` — **compound unique index** to prevent duplicate attendance records
- `{ CourseID: 1, Date: 1 }` — for course session attendance reports
- `{ AttendanceStatus: 1 }` — for attendance statistics

---

## 7. ETL Impact

### What changes in the ETL pipeline:

| Source File | Old Target | New Target | Changes Required |
|---|---|---|---|
| `students.csv` | Student collection | Student collection | Add `ClassID` mapping; remove `Major` field |
| `courses.csv` | Course collection | Course collection | Map `Department` → `DepartmentID`; Map `Instructor` → `TeacherID` |
| `enrollments.csv` | Enrollment collection | Enrollment collection | Keep existing fields; add `MidtermScore`, `FinalScore`, `TotalScore`, `LetterGrade` from grades.csv aggregation |
| `grades.csv` | Grades collection | **REMOVED** | Data must be aggregated per (StudentID, CourseID) pair and merged into Enrollment |
| `attendance.csv` | Attendance collection | Attendance collection | No changes needed |
| `feedback.csv` | Feedback collection | **REMOVED** | No ETL needed; file can be archived |
| **NEW** | — | Department collection | Extract unique departments from courses.csv |
| **NEW** | — | Class collection | Generate synthetic class data based on student majors |
| **NEW** | — | Teacher collection | Extract unique instructors from courses.csv |

### Key ETL Challenges:

1. **Grade Aggregation:** The old `grades.csv` has multiple rows per (StudentID, CourseID) with different `AssignmentType` values. The ETL must:
   - Find the `Midterm` score for each student-course pair.
   - Find the `Final Exam` score for each student-course pair.
   - Compute `TotalScore` as a weighted average (e.g., 40% Midterm + 60% Final).
   - Derive `LetterGrade` from `TotalScore` using a standard scale.
   - Merge this into the Enrollment document.

2. **Class Assignment:** Since the original data has no class information, the ETL must generate class data. A reasonable approach:
   - Group students by their `Major` field.
   - Assign students to classes based on major and a sequential section number.
   - Create corresponding Class and Department documents.

3. **Teacher Creation:** The `courses.csv` has 50 unique instructors. The ETL must:
   - Extract unique instructor names.
   - Generate TeacherID for each.
   - Assign each teacher to a department based on the courses they teach.

---

## 8. MongoDB Document Examples

### Department
```json
{
  "_id": "DEPT001",
  "DepartmentName": "Computer Science",
  "Description": "Study of computers and computational systems"
}
```

### Class
```json
{
  "_id": "CLASS001",
  "ClassName": "CS2024A",
  "DepartmentID": "DEPT001",
  "AcademicYear": 2024,
  "Section": "A"
}
```

### Student
```json
{
  "_id": "STU1001",
  "FirstName": "Alice",
  "LastName": "Johnson",
  "Gender": "Female",
  "DateOfBirth": ISODate("2003-05-14"),
  "ClassID": "CLASS001",
  "GPA": 3.45
}
```

### Teacher
```json
{
  "_id": "TCH001",
  "FirstName": "John",
  "LastName": "Smith",
  "Email": "john.smith@university.edu",
  "Specialization": "Database Systems",
  "DepartmentID": "DEPT001"
}
```

### Course
```json
{
  "_id": "COURSE1",
  "CourseName": "Introduction to Programming",
  "DepartmentID": "DEPT001",
  "Credits": 3,
  "TeacherID": "TCH001"
}
```

### Enrollment
```json
{
  "_id": "ENR001",
  "StudentID": "STU1001",
  "CourseID": "COURSE1",
  "Semester": "Fall",
  "Year": 2024,
  "MidtermScore": 82,
  "FinalScore": 91,
  "TotalScore": 87.4,
  "LetterGrade": "B+"
}
```

### Attendance
```json
{
  "_id": "ATT001",
  "StudentID": "STU1001",
  "CourseID": "COURSE1",
  "Date": ISODate("2024-09-15"),
  "AttendanceStatus": "Present"
}
```

---

## 9. Summary of Changes

| Change | Reason | Impact |
|---|---|---|
| **Remove Feedback** | Not core to academic operations | Simplifies schema; feedback can be added later |
| **Remove Grades** | Fragmented and unrealistic; merge into Enrollment | Simplifies grade queries; single source of truth |
| **Redesign Enrollment** | Add MidtermScore, FinalScore, TotalScore, LetterGrade | Enables GPA calculation and performance analytics |
| **Add Department** | Normalize department data | Eliminates string duplication; enables department analytics |
| **Add Class** | Real university structure | Students belong to classes; enables class-level queries |
| **Add Teacher** | Normalize teacher data | Eliminates string duplication; enables teacher analytics |
| **Student → ClassID** | Link student to class | Creates proper hierarchy: Dept → Class → Student |
| **Course → TeacherID** | Reference instead of string | Proper normalization; enables teacher-course queries |
| **Course → DepartmentID** | Reference instead of string | Proper normalization; enables department-course queries |

---

## 10. Next Steps (Not to be implemented yet)

1. Create MongoDB database and collections with the defined schema.
2. Write ETL scripts to transform CSV data into the new schema.
3. Implement Hadoop/MapReduce jobs for analytics on the new schema.
4. Build Streamlit dashboard for data visualization.
5. Write import scripts for loading data into MongoDB.

---

*Document generated for schema redesign phase. No code implementation has been started.*