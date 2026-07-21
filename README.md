# Hệ thống Quản lý điểm Sinh viên sử dụng Hadoop MapReduce

## Mục lục

1. [Giới thiệu đề tài](#1-giới-thiệu-đề-tài)
2. [Công nghệ sử dụng](#2-công-nghệ-sử-dụng)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Thiết kế cơ sở dữ liệu](#4-thiết-kế-cơ-sở-dữ-liệu)
5. [Bộ dữ liệu sử dụng](#5-bộ-dữ-liệu-sử-dụng)
6. [Quy trình Map Reduce](#6-quy-trình-map-reduce)
7. [Kiến trúc Hadoop MapReduce](#7-kiến-trúc-hadoop-mapreduce)
8. [Các bài toán MapReduce](#8-các-bài-toán-mapreduce)
9. [Cấu trúc thư mục](#9-cấu-trúc-thư-mục)
10. [Hướng dẫn cài đặt](#10-hướng-dẫn-cài-đặt)
11. [Hướng dẫn chạy chương trình](#11-hướng-dẫn-chạy-chương-trình)
12. [Kết quả đạt được](#13-kết-quả-đạt-được)
13. [Kiểm thử](#14-kiểm-thử)
14. [Hạn chế](#15-hạn-chế)
15. [Thành viên thực hiện](#17-thành-viên-thực-hiện)

---

# 1. Giới thiệu đề tài

## 1.1 Mục tiêu

Đề tài xây dựng một hệ thống quản lý sinh viên kết hợp với Hadoop MapReduce nhằm xử lý và phân tích dữ liệu học tập trên tập dữ liệu có kích thước lớn.

Thay vì chỉ thực hiện các thao tác CRUD thông thường trên cơ sở dữ liệu, hệ thống tập trung khai thác dữ liệu thông qua các bài toán thống kê bằng mô hình MapReduce.

---

## 1.2 Bài toán đặt ra

Trong thực tế, dữ liệu sinh viên của một trường đại học có thể bao gồm hàng nghìn đến hàng trăm nghìn bản ghi.

Nếu thực hiện các phép thống kê trực tiếp trên cơ sở dữ liệu sẽ làm giảm hiệu năng khi dữ liệu tăng lên.

Vì vậy đề tài sử dụng Hadoop Streaming để phân tán quá trình xử lý dữ liệu theo mô hình MapReduce.

---

## 1.3 Phạm vi đề tài

Hệ thống bao gồm:

- Quản lý dữ liệu sinh viên
- Quản lý lớp học
- Quản lý môn học
- Quản lý giảng viên
- Quản lý đăng ký học phần
- Thống kê dữ liệu bằng Hadoop MapReduce
- Hiển thị kết quả phân tích

---

# 2. Công nghệ sử dụng

| Công nghệ           | Vai trò                                   |
| ------------------- | ----------------------------------------- |
| Python              | Xây dựng Mapper, Reducer và xử lý dữ liệu |
| MongoDB             | Lưu trữ dữ liệu nghiệp vụ                 |
| Apache Hadoop 3.3.6 | Framework xử lý phân tán                  |
| HDFS                | Hệ thống lưu trữ dữ liệu phân tán         |
| Hadoop Streaming    | Cho phép sử dụng Python với MapReduce     |
| Streamlit           | Xây dựng Dashboard                        |

---

# 3. Kiến trúc hệ thống

## 3.1 Kiến trúc tổng thể

```

CSV Dataset
│
▼
CSV Parser
│
▼
MongoDB
│
▼
Export CSV
│
▼
HDFS
│
▼
Hadoop Streaming
│
├── Mapper (Python)
├── Shuffle & Sort (Hadoop)
└── Reducer (Python)
│
▼
Output
│
▼
MongoDB Analytics
│
▼
Streamlit Dashboard

```

---

## 3.2 Luồng xử lý dữ liệu

Bước 1

Đọc dữ liệu CSV.

↓

Bước 2

Phân tích từng dòng dữ liệu bằng Parser.

↓

Bước 3

Lưu dữ liệu vào MongoDB.

↓

Bước 4

Đưa dữ liệu lên HDFS.

↓

Bước 5

Thực hiện Hadoop Streaming.

↓

Bước 6

Mapper xử lý dữ liệu.

↓

Bước 7

Hadoop tự động thực hiện Shuffle và Sort.

↓

Bước 8

Reducer tổng hợp kết quả.

↓

Bước 9

Kết quả được lưu trên HDFS và phục vụ Dashboard.

---

## 3.3 Vai trò của từng thành phần

### CSV Dataset

Chứa dữ liệu đầu vào của hệ thống.

---

### CSV Parser

Đọc từng dòng dữ liệu và chuyển thành Dictionary để Mapper sử dụng.

---

### MongoDB

Lưu trữ dữ liệu gốc phục vụ cho việc quản lý.

---

### HDFS

Lưu trữ dữ liệu đầu vào và kết quả đầu ra của Hadoop.

---

### Hadoop Streaming

Cho phép sử dụng chương trình Python làm Mapper và Reducer.

---

### Streamlit

Hiển thị kết quả thống kê dưới dạng Dashboard.

---

# 4. Thiết kế cơ sở dữ liệu

Hệ thống sử dụng MongoDB với các Collection sau.

| Collection | Mô tả       |
| ---------- | ----------- |
| Department | Khoa        |
| Class      | Lớp         |
| Teacher    | Giảng viên  |
| Student    | Sinh viên   |
| Course     | Môn học     |
| Enrollment | Đăng ký học |
| Attendance | Điểm danh   |

---

# 5. Bộ dữ liệu sử dụng

Các tập dữ liệu đầu vào gồm:

| File           |
| -------------- |
| Department.csv |
| Class.csv      |
| Teacher.csv    |
| Student.csv    |
| Course.csv     |
| Enrollment.csv |
| Attendance.csv |

---

Trong đó:

**Enrollment.csv** là tập dữ liệu chính phục vụ cho các bài toán MapReduce.

Các trường dữ liệu bao gồm:

- EnrollmentID
- StudentID
- CourseID
- Semester
- Year
- MidtermScore
- FinalScore
- TotalScore
- LetterGrade

---

# 6. Quy trình Map Reduce

Quy trình xử lý của hệ thống được thực hiện theo các bước sau.

```

CSV

↓

CSV Parser

↓

Dictionary

↓

Mapper

↓

Shuffle & Sort

↓

Reducer

↓

Output

```

---

### Bước 1

Đọc dữ liệu từ file CSV.

---

### Bước 2

Parser chuyển đổi dữ liệu thành Dictionary.

Ví dụ:

```python
{
    "student_id": 1,
    "course_id": "COURSE10",
    "total_score": 8.5
}
```

---

### Bước 3

Mapper đọc từng Dictionary.

Mapper phát sinh cặp khóa - giá trị.

Ví dụ:

```
COURSE10    8.5
```

---

### Bước 4

Hadoop thực hiện:

- Partition
- Shuffle
- Sort

---

### Bước 5

Reducer nhận dữ liệu đã được nhóm theo khóa.

Ví dụ:

```
COURSE10

8.5
9.2
7.5
6.8
```

Reducer tính toán và xuất kết quả cuối cùng.

---

# 7. Kiến trúc Hadoop MapReduce

## 7.1 Local Simulation

Đây là chế độ mô phỏng MapReduce bằng Python.

Luồng xử lý:

```

Mapper

↓

Sort

↓

Reducer

```

Mục đích:

- Kiểm thử nhanh.
- Không cần HDFS.
- Không cần Hadoop.

---

## 7.2 Hadoop Streaming

Đây là chế độ chạy chính thức của hệ thống.

Luồng xử lý:

```

HDFS

↓

InputSplit

↓

Mapper (Python)

↓

Shuffle

↓

Reducer (Python)

↓

Output trên HDFS

```

---

## 7.3 Vai trò của Hadoop Framework

Hadoop chịu trách nhiệm:

- Chia Input Split
- Quản lý Task
- Gọi Mapper
- Shuffle
- Sort
- Gọi Reducer
- Ghi Output lên HDFS

---

## 7.4 Vai trò của Mapper và Reducer

Mapper

- Đọc dữ liệu đầu vào.
- Sinh cặp Key - Value.

Reducer

- Nhận dữ liệu đã được nhóm.
- Tổng hợp kết quả.
- Ghi kết quả cuối cùng.

---

# 8. Các bài toán MapReduce

Hiện tại hệ thống đã xây dựng các bài toán sau.

| STT | Bài toán                                 |
| --- | ---------------------------------------- |
| 1   | Đếm số lượng sinh viên theo môn học      |
| 2   | Tính điểm trung bình theo môn học        |
| 3   | Phân bố điểm chữ theo môn học            |
| 4   | Điểm cao nhất theo môn học               |
| 5   | Top N môn học có nhiều sinh viên đăng ký |
| 6   | Thống kê số lượng đăng ký theo học kỳ    |
| 7   | Điểm giữa kỳ trung bình theo môn học     |
| 8   | Phân tích hiệu suất môn học              |
| 9   | Điểm thấp nhất theo môn học              |
| 10  | Thống kê tỷ lệ Đậu / Rớt                 |

Mỗi bài toán đều được xây dựng bằng một cặp Mapper và Reducer riêng, có thể chạy độc lập hoặc chạy đồng thời thông qua tập lệnh `run_all.cmd`.

---

# 9. Cấu trúc thư mục

```
BigData
│
├── data
│   ├── input
│   └── output
│
├── docs
│
├── job
│   └── job
│       ├── average_score
│       ├── avg_midterm_per_course
│       ├── count_course
│       ├── course_performance_analytics
│       ├── grade_distribution
│       ├── highest_score
│       ├── lowest_score_per_course
│       ├── pass_fail_per_course
│       ├── semester_count
│       └── top_n_course
│
├── mongodb
│
├── output
│
├── src
│   ├── analysis
│   ├── dashboard
│   ├── database
│   ├── parser
│   └── utils
│
├── run.cmd
├── run_streaming.cmd
└── README.md
```

---

## Giải thích các thư mục

### data/

Lưu dữ liệu đầu vào và đầu ra của chương trình.

---

### job/

Chứa toàn bộ các chương trình MapReduce.

Mỗi bài toán được đặt trong một thư mục riêng gồm:

- mapper.py
- reducer.py

Ví dụ:

```
count_course
│
├── mapper.py
└── reducer.py
```

---

### src/

Chứa toàn bộ mã nguồn hỗ trợ.

Ví dụ:

- CSV Parser
- MongoDB
- Dashboard
- Các chương trình kiểm tra dữ liệu

---

### mongodb/

Lưu các script phục vụ MongoDB.

---

### run.cmd

Chạy toàn bộ các bài toán MapReduce bằng Local Simulation.

---

### run_streaming.cmd

Chạy toàn bộ các bài toán bằng Hadoop Streaming.

---

# 10. Hướng dẫn cài đặt

## Yêu cầu

Cần cài đặt các thành phần sau:

- Python 3.x
- MongoDB
- Java JDK
- Apache Hadoop 3.3.6
- Winutils (Windows)

---

## Thư viện Python

Cài đặt các thư viện cần thiết.

```
pip install pymongo
pip install streamlit
```

Nếu sử dụng Dashboard có thể cần thêm:

```
pip install pandas
pip install matplotlib
```

---

## Thiết lập Hadoop

Cần cấu hình:

- JAVA_HOME
- HADOOP_HOME
- PATH

Khởi động:

- NameNode
- DataNode

Kiểm tra:

```
hdfs dfs -ls /
```

Nếu hiển thị được thư mục trên HDFS nghĩa là Hadoop đã hoạt động.

---

# 11. Hướng dẫn chạy chương trình

## 11.1 Chạy Local

Đây là chế độ mô phỏng MapReduce bằng Python.

Thực hiện:

```
run.cmd
```

Chương trình sẽ lần lượt thực hiện toàn bộ các bài toán MapReduce.

Kết quả được lưu trong:

```
data/output/
```

Ví dụ:

```
count_course.txt
average_score.txt
highest_score.txt
...
```

---

## 11.2 Chạy từng chức năng riêng lẻ

Mỗi bài toán có thể chạy độc lập bằng cách double-click file `.cmd` tương ứng hoặc gõ lệnh:

Danh sách các file lệnh:

| File lệnh                    | Chức năng                                     |
| ---------------------------- | --------------------------------------------- |
| `run_semester_count.cmd`     | Đếm số lượng sinh viên theo học kỳ            |
| `run_count_course.cmd`       | Đếm số lượng sinh viên theo môn học           |
| `run_average_score.cmd`      | Tính điểm trung bình theo môn học             |
| `run_grade_distribution.cmd` | Phân bố điểm chữ theo môn học                 |
| `run_highest_score.cmd`      | Tìm điểm cao nhất theo môn học                |
| `run_top_n_course.cmd`       | Top N môn học có nhiều sinh viên đăng ký nhất |
| `run_avg_midterm.cmd`        | Tính điểm giữa kỳ trung bình theo môn học     |
| `run_course_performance.cmd` | Phân tích hiệu suất môn học                   |
| `run_lowest_score.cmd`       | Tìm điểm thấp nhất theo môn học               |
| `run_pass_fail.cmd`          | Thống kê tỷ lệ Đậu / Rớt theo môn học         |

Kết quả đầu ra được lưu trong thư mục `output/ten_chuc_nang/part-00000`.

---

## 11.3 Chạy Hadoop Streaming

Đầu tiên cần đưa dữ liệu lên HDFS.

Ví dụ:

```
Enrollment.csv

↓

HDFS

/input/Enrollment.csv
```

Sau đó chạy:

```
run_streaming.cmd
```

Kết quả sẽ được lưu trên HDFS.

Ví dụ:

```
/output/count_course
/output/average_score
/output/highest_score
```

---

## 11.4 Xem kết quả trên HDFS

Ví dụ:

```
hdfs dfs -cat /output/count_course/part-00000
```

Kết quả:

```
COURSE1     12
COURSE2     15
COURSE3     8
...
```

---

# 13. Kết quả đạt được

Đề tài đã xây dựng thành công:

- Hệ thống quản lý dữ liệu sinh viên.
- CSV Parser.
- MongoDB Database.
- HDFS.
- Hadoop Streaming.
- Local Simulation.
- Dashboard.

Hiện tại hệ thống đã triển khai thành công các bài toán MapReduce sau:

- Semester Count
- Count Course
- Average Score
- Average Midterm Score
- Highest Score
- Lowest Score
- Grade Distribution
- Pass / Fail
- Course Performance Analytics
- Top N Course

---

# 14. Kiểm thử

Đề tài được kiểm thử theo hai hình thức.

## Local Simulation

---

## Hadoop Streaming

---

# 15. Hạn chế

Đề tài vẫn còn một số hạn chế:

- Chưa triển khai Hadoop Cluster nhiều máy.
- Chưa sử dụng Spark.
- Chưa tối ưu được hệ thống.
- Chưa xây dựng Dashboard thời gian thực.
- Chỉ dừng lại ở việc đề tài mô phỏng, còn khá nhiều khuyết điểm so với những bài toán thực tế

---

# 17. Thành viên thực hiện

Phan Hoài Huy | Nhóm trưởng
Trần Thiên Phúc | Thành viên

---
