# 📋 Báo cáo cấu hình máy chạy Hadoop (BigDataTest - Windows 11)

> Ngày: 28/07/2026  
> Mục đích: Lưu lại toàn bộ setting & lệnh check để sau này dùng lại

---

## 1. 🖥️ Thông tin máy

| Thông số | Giá trị |
|----------|---------|
| OS | Windows 11 |
| User | `AdMin` |
| Project root | `C:\Users\AdMin\BigDataTest` |

---

## 2. ☕ Java 11

### Vị trí cài đặt

```
D:\Java11\bin\java.exe
```

### Phiên bản
```
OpenJDK 11.0.31 (Temurin)
```

### Lệnh kiểm tra

```cmd
:: Kiểm tra Java version
java -version

:: Kiểm tra JAVA_HOME
echo %JAVA_HOME%

:: Kiểm tra Java ở đâu
where java
```

### ❌ Lưu ý lỗi cũ
Trong các file `.cmd` cũ ghi `C:\PROGRA~1\Java\JRE18~1.0_4` — **SAI**, không tồn tại.  
Đã sửa thành `D:\Java11`.

---

## 3. 🐘 Hadoop 3.3.6

### Vị trí cài đặt

```
D:\hadoop\hadoop-3.3.6
```

### Streaming JAR
```
D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar
```

### Lệnh kiểm tra

```cmd
:: Kiểm tra Hadoop version
hadoop version

:: Kiểm tra HADOOP_HOME
echo %HADOOP_HOME%

:: Kiểm tra Hadoop ở đâu
where hadoop

:: Kiểm tra streaming JAR tồn tại
dir D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-*.jar

:: List HDFS (nếu đã start Hadoop)
hdfs dfs -ls /
```

### ❌ Lưu ý lỗi cũ
Trong các file `.cmd` cũ ghi `C:\hadoop\hadoop-3.3.6` — **SAI**, không tồn tại.  
Đã sửa thành `D:\hadoop\hadoop-3.3.6`.

---

## 4. 🐍 Python

### Phiên bản có sẵn

| Phiên bản | Path | Cách gọi |
|-----------|------|----------|
| **Python 3.14** | `C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe` | `py -3.14` |
| **Python 3.10** | `C:\Users\AdMin\AppData\Local\Programs\Python\Python310\python.exe` | `py -3.10` |

### Python Launcher (khuyên dùng)
```
C:\Windows\py.exe
```

### Lệnh kiểm tra

```cmd
:: Liệt kê các Python đã cài
py --list

:: Kiểm tra Python path cụ thể
py -3.14 -c "import sys;print(sys.executable)"

:: Kiểm tra module parser_1 import được không
py -3.14 C:\Users\AdMin\BigDataTest\test_import.py

:: Kiểm tra pip
py -3.14 -m pip --version
```

### ❌ Lưu ý lỗi cũ
Các file `.cmd` cũ ghi:  
`C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe` — **SAI**, user là `Admin` không tồn tại, Python 3.12 không tồn tại.

Đã sửa:  
`C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe` — **ĐÚNG**

---

## 5. 📂 Cấu trúc dự án (BigDataTest)

### Thư mục quan trọng

| Thư mục | Mô tả |
|---------|-------|
| `data/processed/` | Dữ liệu đầu vào CSV |
| `data/output/` | Output chế độ Local Simulation |
| `output/` | Output chế độ Hadoop Streaming |
| `job/job/*/` | Mapper & Reducer cho từng bài toán |
| `parser_1/` | Module parse CSV (import bởi mapper) |
| `execute/` | Script `.cmd` **gốc** (bị sai path, cần sửa) |

### Các file wrapper mới tạo (đã fix path)

| File | Mô tả |
|------|-------|
| `job/job/count_course/mapper_wrapper.cmd` | Mapper wrapper cho count_course |
| `job/job/count_course/reducer_wrapper.cmd` | Reducer wrapper cho count_course |
| `run_hadoop_count_course.cmd` | Script chạy Hadoop Streaming (gốc project) |

---

## 6. 🚀 Cách chạy Hadoop Streaming (đã test thành công)

### Bước 1: Chạy trực tiếp từ project root
```cmd
cd C:\Users\AdMin\BigDataTest
run_hadoop_count_course.cmd
```

### Bước 2: Xem kết quả
```cmd
type output\count_course\part-00000
```

### Bước 3: Để chạy các bài toán khác (ví dụ highest_score)
Cần tạo tương tự các wrapper `.cmd` cho job tương ứng, rồi copy `run_hadoop_count_course.cmd` và sửa đường dẫn mapper/reducer.

---

## 7. ⚙️ Các biến môi trường CẦN SET (nếu dùng cmd mới)

```cmd
set HADOOP_HOME=D:\hadoop\hadoop-3.3.6
set JAVA_HOME=D:\Java11
set PATH=%PATH%;%HADOOP_HOME%\bin;%JAVA_HOME%\bin
```

> **Quan trọng**: Nếu mở CMD mới, phải set lại các biến này trước khi chạy Hadoop.

---

## 8. 🔍 Cheat Sheet - Các lệnh check nhanh

```cmd
:: ===== CHECK JAVA =====
java -version
where java

:: ===== CHECK HADOOP =====
hadoop version
where hadoop

:: ===== CHECK PYTHON =====
py --list
py -3.14 -c "import sys;print(sys.executable)"

:: ===== CHECK STREAMING JAR =====
dir D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-*.jar

:: ===== CHECK IMPORT PARSER =====
py -3.14 C:\Users\AdMin\BigDataTest\test_import.py

:: ===== CHECK OUTPUT HADOOP =====
type C:\Users\AdMin\BigDataTest\output\count_course\part-00000

:: ===== CHECK FILE ĐẦU VÀO =====
more C:\Users\AdMin\BigDataTest\data\processed\Enrollment.csv
```

---

## 9. 🛠️ Tóm tắt các lỗi đã fix

| # | Lỗi | File bị ảnh hưởng | Cách fix |
|---|-----|-------------------|----------|
| 1 | `HADOOP_HOME` sai: `C:\hadoop\...` | `execute/run.cmd`, `execute/run_streaming.cmd`, `job/job/run_all.cmd` | Sửa thành `D:\hadoop\hadoop-3.3.6` |
| 2 | `JAVA_HOME` sai: `JRE18~1.0_4` | `execute/run.cmd`, `execute/run_streaming.cmd` | Sửa thành `D:\Java11` |
| 3 | `Python` path sai: `Admin\...\Python312` | `execute/run.cmd`, `execute/run_streaming.cmd`, `job/job/run_all.cmd` | Sửa thành `AdMin\...\pythoncore-3.14-64` |
| 4 | `PROJECT_ROOT` sai: `Desktop\BigData\BigDataProject` | `job/job/run_all.cmd` | Sửa thành `C:\Users\AdMin\BigDataTest` |
| 5 | Python path có spaces (Program Files) không quote | Các wrapper `.cmd` | Thêm quotes kép: `"...\python.exe" "...\mapper.py"` |
| 6 | Hadoop dùng HDFS mặc định | `run_hadoop_count_course.cmd` | Thêm `-D fs.defaultFS=file:///` và `-D mapreduce.framework.name=local` |
| 7 | Module `parser_1` không tìm thấy | Wrapper script | Thêm `set PYTHONPATH=C:\Users\AdMin\BigDataTest` |

---

> **Mẹo**: Để fix nhanh tất cả file `.cmd` gốc trong thư mục `execute/`, cách đơn giản nhất là sửa 4 dòng đầu:
> ```diff
> - set HADOOP_HOME=C:\hadoop\hadoop-3.3.6
> + set HADOOP_HOME=D:\hadoop\hadoop-3.3.6
> - set JAVA_HOME=C:\PROGRA~1\Java\JRE18~1.0_4
> + set JAVA_HOME=D:\Java11
> - set PYTHON=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
> + set PYTHON=C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe
