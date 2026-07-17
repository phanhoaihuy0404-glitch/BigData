# Hadoop Streaming Debug Report

**Generated:** 2026-07-16 22:27 ICT  
**Project:** University Big Data Project - Student Management System  
**Phase:** Hadoop Streaming - Job #1 (Count students per course)

---

## SECTION 1: Environment

### Operating System
- **OS Name:** Microsoft Windows 11 Home Single Language
- **OS Version:** 10.0.26200 Build 26200

### Java
- **Version:** OpenJDK 11.0.31 (Temurin-11.0.31+11)
- **JAVA_HOME:** `D:\Java11`

### Hadoop
- **Version:** Hadoop 3.3.6
- **HADOOP_HOME:** `D:\hadoop\hadoop-3.3.6`
- **Compiled:** 2023-06-18 on linux-x86_64

### Python
- **Version:** Python 3.14.2
- **Note:** `python` command not found, only `python3` works

### Current Working Directory
- **Path:** `E:\BigDataProject`

---

## SECTION 2: HDFS Status

### Running Processes (jps -lv)
```
12476 org.apache.hadoop.hdfs.server.namenode.NameNode
  -Xmx1000m
  -Dhadoop.log.dir=D:\hadoop\hadoop-3.3.6\logs
  -Dhadoop.home.dir=D:\hadoop\hadoop-3.3.6
  -Dhadoop.id.str=AdMin
  -Djava.net.preferIPv4Stack=true

29676 org.apache.hadoop.hdfs.server.datanode.DataNode
  -Xmx1000m
  -Dhadoop.log.dir=D:\hadoop\hadoop-3.3.6\logs
  -Dhadoop.home.dir=D:\hadoop\hadoop-3.3.6
  -Dhadoop.id.str=AdMin
  -Djava.net.preferIPv4Stack=true

23612 jdk.jcmd/sun.tools.jps.Jps
```

**Status:** ✅ NameNode and DataNode running

### Cluster Report (hdfs dfsadmin -report)
```
Configured Capacity: 107373129728 (100.00 GB)
Present Capacity: 94608818331 (88.11 GB)
DFS Remaining: 94608793600 (88.11 GB)
DFS Used: 24731 (24.15 KB)
DFS Used%: 0.00%

Live datanodes (1):
  Name: 127.0.0.1:9866 (127.0.0.1)
  Hostname: LAPTOP-LI05IQCM
  Decommission Status: Normal
  Configured Capacity: 107373129728 (100.00 GB)
  DFS Used: 24731 (24.15 KB)
  Non DFS Used: 12764311397 (11.89 GB)
  DFS Remaining: 94608793600 (88.11 GB)
  DFS Used%: 0.00%
  Num of Blocks: 4
```

**Status:** ✅ Healthy - 1 DataNode, no under-replicated blocks

### SafeMode Status
```
Safe mode is OFF
```

**Status:** ✅ SafeMode disabled, cluster ready for operations

---

## SECTION 3: Project Structure

```
E:\BIGDATAPROJECT
│   .gitignore
│   AI_Rules
│   mapper.py                    ← Working directory copy
│   reducer.py                   ← Working directory copy
│   StudentManagementDB.db
│   test.txt
│   test_downloaded.txt
│   validation_downloaded.txt
│   validation_file.txt
│
├───data
│   ├───output
│   │       Attendance.csv
│   │       Class.csv
│   │       Course.csv
│   │       Department.csv
│   │       Enrollment.csv
│   │       Student.csv
│   │       Teacher.csv
│   │
│   └───processed
│           Attendance.csv
│           Class.csv
│           Course.csv
│           Department.csv
│           Enrollment.csv
│           Student.csv
│           Teacher.csv
│
├───docs
│       schema_redesign.md
│
├───mongodb
│   │   config.py
│   │   connect.py
│   │   export_data.py
│   │   import_data.py
│   │   query_examples.py
│   │
│   └───__pycache__
│           config.cpython-314.pyc
│           connect.cpython-314.pyc
│           export_data.cpython-314.pyc
│           import_data.cpython-314.pyc
│           query_examples.cpython-314.pyc
│           quick_check.cpython-314.pyc
│
└───src
    ├───analysis
    │       check_new_schema.py
    │       validate_database.py
    │
    ├───etl
    │       transform_raw_to_processed.py
    │
    └───hadoop
            mapper.py
            reducer.py
```

**Note:** mapper.py and reducer.py exist in BOTH:
- `E:\BigDataProject\mapper.py` (root)
- `E:\BigDataProject\src\hadoop\mapper.py` (src/hadoop/)

---

## SECTION 4: Mapper / Reducer Details

### mapper.py
- **Absolute Path:** `E:\BigDataProject\mapper.py`
- **Exists:** ✅ Yes
- **File Size:** 588 bytes
- **Last Modified:** 7/16/2026 9:24:29 PM
- **Current Working Directory:** `E:\BigDataProject`

### reducer.py
- **Absolute Path:** `E:\BigDataProject\reducer.py`
- **Exists:** ✅ Yes
- **File Size:** 1099 bytes
- **Last Modified:** 7/16/2026 9:24:56 PM
- **Current Working Directory:** `E:\BigDataProject`

### File Permissions (icacls output)
```
E:\BigDataProject\mapper.py
  BUILTIN\Administrators:(I)(F)
  NT AUTHORITY\SYSTEM:(I)(F)
  NT AUTHORITY\Authenticated Users:(I)(M)
  BUILTIN\Users:(I)(RX)
```

**Note:** Users group has only Read & Execute (RX), NOT Full Control

---

## SECTION 5: Streaming Command

### Last Attempted Command
```bash
hadoop jar D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar \
  -file mapper.py \
  -file reducer.py \
  -mapper "python mapper.py" \
  -reducer "python reducer.py" \
  -input /input/Enrollment.csv \
  -output /output/course_counts
```

**Note:** This command was executed from `E:\BigDataProject` directory

---

## SECTION 6: Streaming Jar

### hadoop-streaming-3.3.6.jar
- **Absolute Path:** `D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar`
- **Exists:** ✅ Yes
- **File Size:** Not measured

---

## SECTION 7: Error Log

### Complete Error Output
```
2026-07-16 22:14:27,434 WARN streaming.StreamJob: -file option is deprecated, 
  please use generic option -files instead.
File: file:/E:/BigDataProject/mapper.py is not readable.
Try -help for more information
Streaming Command Failed!
```

### Stack Trace
```
Exception in thread "main" java.lang.IllegalArgumentException: 
  java.net.URISyntaxException: Illegal character in scheme name at index 0: 
  file:///D:/hadoop/hadoop-3.3.6/mapper.py
```

**Note:** No full Java stack trace provided in the output

---

## SECTION 8: Commands History

### Attempted Commands

| # | Command | Status | Reason |
|---|---------|--------|--------|
| 1 | `hadoop jar ... -files D:/hadoop/hadoop-3.3.6/mapper.py,D:/hadoop/hadoop-3.3.6/reducer.py` | ❌ Failed | UnsupportedFileSystemException: No FileSystem for scheme "D" |
| 2 | `hadoop jar ... -files file:///D:/hadoop/hadoop-3.3.6/mapper.py,file:///D:/hadoop/hadoop-3.3.6/reducer.py` | ❌ Failed | Found 1 unexpected arguments on the command line |
| 3 | `hadoop jar ... -file D:/hadoop/hadoop-3.3.6/mapper.py -file D:/hadoop/hadoop-3.3.6/reducer.py` | ❌ Failed | UnsupportedFileSystemException: No FileSystem for scheme "D" |
| 4 | `hadoop jar ... -file file:///D:/hadoop/hadoop-3.3.6/mapper.py -file file:///D:/hadoop/hadoop-3.3.6/reducer.py` | ❌ Failed | Found 1 unexpected arguments on the command line |
| 5 | `hadoop jar ... -files /input/mapper.py,/input/reducer.py` | ❌ Failed | FileNotFoundException: File /input/mapper.py does not exist |
| 6 | `hadoop jar ... -files E:/BigDataProject/mapper.py,E:/BigDataProject/reducer.py` | ❌ Failed | UnsupportedFileSystemException: No FileSystem for scheme "E" |
| 7 | `hadoop jar ... -files file:///E:/BigDataProject/mapper.py,file:///E:/BigDataProject/reducer.py` | ❌ Failed | Found 1 unexpected arguments on the command line |
| 8 | `hadoop jar ... -file mapper.py -file reducer.py` (from D:\hadoop\hadoop-3.3.6) | ❌ Failed | File: file:/E:/BigDataProject/mapper.py is not readable |
| 9 | `hadoop jar ... -file mapper.py -file reducer.py` (from E:\BigDataProject) | ❌ Failed | File: file:/E:/BigDataProject/mapper.py is not readable |
| 10 | `hadoop jar ... -file E:\BigDataProject\mapper.py -file E:\BigDataProject\reducer.py` | ❌ Failed | File: file:/E:/BigDataProject/mapper.py is not readable |

**Total attempts:** 10+  
**Successful:** 0  
**Failed:** 10+

---

## SECTION 9: Root Cause Analysis

### Question 1: Where exactly is Hadoop trying to load mapper.py from?

**Answer:** Hadoop is trying to load mapper.py from:
```
file:/E:/BigDataProject/mapper.py
```

This is confirmed by the error message:
```
File: file:/E:/BigDataProject/mapper.py is not readable
```

### Question 2: Where is mapper.py actually located?

**Answer:** mapper.py is located at:
```
E:\BigDataProject\mapper.py
```

### Question 3: Are those paths identical?

**Answer:** 
- Hadoop tries to access: `file:/E:/BigDataProject/mapper.py` (with forward slashes and `file:` prefix)
- Actual location: `E:\BigDataProject\mapper.py` (with backslashes)

**The paths are NOT identical.** Hadoop converts the Windows path to a URI format.

### Question 4: If not, show both paths

**Hadoop's attempted path:**
```
file:/E:/BigDataProject/mapper.py
```

**Actual file system path:**
```
E:\BigDataProject\mapper.py
```

### Question 5: Does Hadoop think the file does not exist or exists but is unreadable?

**Answer:** Hadoop thinks the file **exists but is unreadable**.

The error message states:
```
File: file:/E:/BigDataProject/mapper.py is not readable
```

This is NOT a "FileNotFoundException". The file is found, but Hadoop cannot read it.

### Question 6: Is the error generated before Mapper execution or after Mapper execution starts?

**Answer:** The error is generated **BEFORE Mapper execution starts**.

This is a **job setup/initialization error**, not a runtime error. Hadoop validates the `-file` arguments during job submission, before any MapReduce tasks are launched.

---

## SECTION 10: Root Cause Determination

### Primary Cause: **E. Actual filesystem permission problem**

### Evidence:

1. **Error message:** "is not readable" (not "does not exist")
2. **File permissions:** Users group has only `(I)(RX)` - Read and Execute, NOT Full Control
3. **Hadoop runs as:** Different user context (likely SYSTEM or service account)
4. **Working directory:** `E:\BigDataProject` is the current directory
5. **File location:** mapper.py is in the working directory

### Why Hadoop Cannot Read the File:

1. **Permission Issue:** The file `E:\BigDataProject\mapper.py` has permissions:
   - Administrators: Full Control (F)
   - SYSTEM: Full Control (F)
   - Authenticated Users: Modify (M)
   - Users: Read & Execute (RX) only

2. **Hadoop Process User:** The Hadoop daemons (NameNode, DataNode) run as a service, likely under the `SYSTEM` account or a service account that may not have the same permissions as the interactive user.

3. **File Access:** When Hadoop Streaming tries to distribute the mapper.py file to the cluster nodes, it attempts to read the file from the local filesystem. The process does not have sufficient permissions to read the file.

### Why This Happens on Windows:

On Windows, file permissions are more restrictive than on Linux. Even though the file exists and is readable by the current user, the Hadoop service account may not have the necessary permissions.

### Why Previous Fixes Failed:

1. **icacls /grant Users:R** - Only gave Read permission to Users group, but Hadoop may not be running as a Users group member
2. **icacls /grant Everyone:F** - Should have worked, but may not have been applied correctly or Hadoop process may have cached the old permissions
3. **Copying to D:\hadoop\hadoop-3.3.6** - Same permission issues apply

### The Core Problem:

**Hadoop Streaming on Windows requires the mapper/reducer scripts to be readable by the Hadoop service account, not just the interactive user.**

---

## DELIVERABLE: Summary

### Problem Statement
Hadoop Streaming job fails during job submission with error:
```
File: file:/E:/BigDataProject/mapper.py is not readable
```

### Root Cause
**Filesystem permission issue.** The Hadoop service account does not have read access to `E:\BigDataProject\mapper.py`, even though the file exists and is readable by the interactive user.

### Evidence
1. Error message explicitly states "is not readable" (not "does not exist")
2. File permissions show Users group has only RX, not Full Control
3. Hadoop daemons run as service accounts with different privileges
4. Error occurs during job initialization, before any MapReduce tasks start

### Impact
- Hadoop Streaming job cannot be submitted
- Mapper and reducer scripts are not distributed to cluster nodes
- No MapReduce execution occurs

### Next Steps Required
The fix requires ensuring the Hadoop service account has read permissions to the mapper.py and reducer.py files, OR running the Hadoop command from a location where the service account has full access (e.g., `C:\hadoop\scripts\` with proper ACLs).

---

**END OF DEBUG REPORT**