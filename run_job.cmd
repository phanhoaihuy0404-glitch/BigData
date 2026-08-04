@echo off
REM ============================================================
REM Hadoop Streaming Job Runner (HDFS Version)
REM Usage:
REM     run_job.cmd <job_name>
REM ============================================================

setlocal EnableDelayedExpansion

REM ============================================================
REM Check Parameter
REM ============================================================

if "%1"=="" (
    echo Usage: run_job.cmd ^<job_name^>
    REM pause
    exit /b 1
)


set JOB_NAME=%1

REM Tham so thu 2 (tuy chon): so luong reducer. Mac dinh la 2 neu khong truyen.
REM Vi du: run_job.cmd count_students_by_course 5
set NUM_REDUCERS=%2
if "%NUM_REDUCERS%"=="" set NUM_REDUCERS=2


REM ============================================================
REM Configuration
REM ============================================================

set HADOOP_HOME=D:\hadoop\hadoop-3.3.6
set JAVA_HOME=D:\Java11

set PYTHON=C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe


set PATH=%HADOOP_HOME%\bin;%JAVA_HOME%\bin;%PATH%


set PROJECT_ROOT=C:\Users\AdMin\BigDataTest


set JOB_DIR=%PROJECT_ROOT%\job\%JOB_NAME%


set LOCAL_INPUT=%PROJECT_ROOT%\data\output\Enrollment.csv

set LOCAL_OUTPUT=%PROJECT_ROOT%\output\%JOB_NAME%


set HDFS_INPUT=/input/Enrollment.csv

set HDFS_OUTPUT=/output/%JOB_NAME%



REM ============================================================
REM Check Job
REM ============================================================

if not exist "%JOB_DIR%\mapper.py" (
    echo.
    echo [FAIL] mapper.py not found
    REM pause
    exit /b 1
)


if not exist "%JOB_DIR%\reducer.py" (
    echo.
    echo [FAIL] reducer.py not found
    REM pause
    exit /b 1
)



REM ============================================================
REM Export MongoDB
REM ============================================================

echo.
echo ============================================================
echo Export MongoDB
echo ============================================================


"%PYTHON%" -m mongodb.export_data


if errorlevel 1 (
    echo.
    echo [FAIL] MongoDB export failed
    REM pause
    exit /b 1
)


echo.
echo [OK] MongoDB export completed



REM ============================================================
REM Upload CSV To HDFS
REM ============================================================


echo.
echo ============================================================
echo Upload CSV To HDFS
echo ============================================================


echo Removing old input...

call hdfs dfs -rm -f %HDFS_INPUT%


echo Uploading CSV...


call hdfs dfs -put "%LOCAL_INPUT%" /input


if errorlevel 1 (
    echo.
    echo [FAIL] Upload HDFS failed
    REM pause
    exit /b 1
)



echo.
echo Verify HDFS input:

call hdfs dfs -ls /input




REM ============================================================
REM Remove Old Output
REM ============================================================

echo.
echo ============================================================
echo Remove Old Output
echo ============================================================

call hdfs dfs -rm -r -f -skipTrash %HDFS_OUTPUT% >nul 2>&1

set RETRY_COUNT=0

:CHECK_OUTPUT_DELETED

call hdfs dfs -test -e %HDFS_OUTPUT% >nul 2>&1

if not errorlevel 1 (

    set /a RETRY_COUNT+=1

    if !RETRY_COUNT! GEQ 10 (
        echo [FAIL] Could not confirm output directory deletion after 10 retries
        exit /b 1
    )

    echo Output directory still exists, waiting and retrying... !RETRY_COUNT!/10

    call hdfs dfs -rm -r -f -skipTrash %HDFS_OUTPUT% >nul 2>&1

    ping -n 2 127.0.0.1 >nul

    goto CHECK_OUTPUT_DELETED
)

if exist "%LOCAL_OUTPUT%" (
    rmdir /s /q "%LOCAL_OUTPUT%"
)

echo.
echo [OK] Old output removed



REM ============================================================
REM Hadoop Streaming
REM ============================================================


echo.
echo ============================================================
echo Hadoop Streaming
echo ============================================================


echo.
echo Job      : %JOB_NAME%
echo Mapper   : %JOB_DIR%\mapper.py
echo Reducer  : %JOB_DIR%\reducer.py
echo Input    : %HDFS_INPUT%
echo Output   : %HDFS_OUTPUT%
echo Reducers : %NUM_REDUCERS%
echo.



REM Move into job directory
cd /d "%JOB_DIR%"


echo Current directory:
cd



call hadoop jar "%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" ^
-D mapreduce.job.reduces=%NUM_REDUCERS% ^
-file mapper.py ^
-file reducer.py ^
-file "%PROJECT_ROOT%\parser_1\csv_parser.py" ^
-input %HDFS_INPUT% ^
-output %HDFS_OUTPUT% ^
-mapper "%PYTHON% mapper.py" ^
-reducer "%PYTHON% reducer.py"


if errorlevel 1 (
    echo.
    echo [FAIL] Hadoop Streaming failed

    cd /d "%PROJECT_ROOT%"

    REM pause
    exit /b 1
)

REM Dọn file rác csv_parser.py được Hadoop copy tạm vào thư mục job
if exist "csv_parser.py" del /q "csv_parser.py"

REM Return project root

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



if errorlevel 1 (
    echo.
    echo [FAIL] Download result failed
    REM pause
    exit /b 1
)




REM ============================================================
REM Display Result
REM ============================================================


echo.
echo ============================================================


if exist "%LOCAL_OUTPUT%\part-00000" (

    echo Result ^(tat ca %NUM_REDUCERS% file part-*^):
    echo.

    for %%F in ("%LOCAL_OUTPUT%\part-*") do (
        echo --- %%~nxF ---
        type "%%F"
    )


) else (

    echo [FAIL] part-00000 not found

)



echo.
echo ============================================================
echo Finished
echo ============================================================



REM pause

endlocal