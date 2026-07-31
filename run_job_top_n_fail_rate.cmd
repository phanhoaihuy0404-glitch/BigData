@echo off
REM ============================================================
REM Hadoop Streaming Job Runner - top_n_fail_rate (Job 2)
REM
REM Job nay doc TRUC TIEP output cua Job 1 (pass_fail_per_course)
REM tren HDFS, KHONG upload lai CSV tho vao /input.
REM
REM Usage:
REM     run_job_top_n_fail_rate.cmd <N>
REM
REM Example:
REM     run_job_top_n_fail_rate.cmd 5
REM ============================================================

setlocal

REM ============================================================
REM Check Parameter
REM ============================================================

set TOP_N=%1

if "%TOP_N%"=="" (
    echo Usage:
    echo run_job_top_n_fail_rate.cmd ^<N^>
    echo Vi du: run_job_top_n_fail_rate.cmd 5
    exit /b 1
)

REM ============================================================
REM Configuration
REM ============================================================

set HADOOP_HOME=D:\hadoop\hadoop-3.3.6
set JAVA_HOME=D:\Java11

set PYTHON=C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe

set PATH=%HADOOP_HOME%\bin;%JAVA_HOME%\bin;%PATH%

set PROJECT_ROOT=C:\Users\AdMin\BigDataTest

set JOB_NAME=top_n_fail_rate
set JOB_DIR=%PROJECT_ROOT%\job\%JOB_NAME%

REM Input cua Job2 la OUTPUT cua Job1 (pass_fail_per_course), khong phai /input
set HDFS_INPUT=/output/pass_fail_per_course
set HDFS_OUTPUT=/output/%JOB_NAME%

set LOCAL_OUTPUT=%PROJECT_ROOT%\output\%JOB_NAME%

REM ============================================================
REM Check Job Files
REM ============================================================

if not exist "%JOB_DIR%\mapper.py" (
    echo mapper.py not found tai %JOB_DIR%
    exit /b 1
)

if not exist "%JOB_DIR%\reducer.py" (
    echo reducer.py not found tai %JOB_DIR%
    exit /b 1
)

REM ============================================================
REM Verify Job1 Output Exists (input cua Job2)
REM ============================================================

echo.
echo ============================================================
echo Kiem tra input cua Job2: %HDFS_INPUT%
echo ============================================================

call hdfs dfs -test -e %HDFS_INPUT%

if errorlevel 1 (
    echo.
    echo LOI: Khong tim thay %HDFS_INPUT% tren HDFS.
    echo Hay chay Job1 ^(pass_fail_per_course^) truoc khi chay Job2.
    exit /b 1
)

call hdfs dfs -ls %HDFS_INPUT%

REM ============================================================
REM Remove Old Output
REM ============================================================

echo.
echo ============================================================
echo Remove Old Output
echo ============================================================

call hdfs dfs -rm -r -f %HDFS_OUTPUT%

if exist "%LOCAL_OUTPUT%" (
    rmdir /s /q "%LOCAL_OUTPUT%"
)

REM ============================================================
REM Hadoop Streaming
REM ============================================================

echo.
echo ============================================================
echo Hadoop Streaming: %JOB_NAME% (Top %TOP_N%)
echo ============================================================

cd /d "%JOB_DIR%"

call hadoop jar "%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" ^
-D mapreduce.job.reduces=1 ^
-file mapper.py ^
-file reducer.py ^
-input %HDFS_INPUT% ^
-output %HDFS_OUTPUT% ^
-mapper "%PYTHON% mapper.py" ^
-reducer "%PYTHON% reducer.py %TOP_N%"

if errorlevel 1 (
    echo Hadoop Streaming failed
    cd /d "%PROJECT_ROOT%"
    exit /b 1
)

cd /d "%PROJECT_ROOT%"

REM ============================================================
REM Download Result
REM ============================================================

echo.
echo ============================================================
echo Download Result
echo ============================================================

mkdir "%LOCAL_OUTPUT%" >nul 2>&1

call hdfs dfs -get %HDFS_OUTPUT%/* "%LOCAL_OUTPUT%"

REM ============================================================
REM Display Result
REM ============================================================

echo.
echo ============================================================

if exist "%LOCAL_OUTPUT%\part-00000" (
    echo Ket qua Top %TOP_N% khoa hoc co ty le truot cao nhat:
    echo.
    type "%LOCAL_OUTPUT%\part-00000"
) else (
    echo part-00000 not found
)

echo.
echo ============================================================
echo Finished
echo ============================================================

endlocal