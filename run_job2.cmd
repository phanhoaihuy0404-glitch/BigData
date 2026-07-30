@echo off
REM ============================================================
REM Hadoop Streaming Multi Input Job Runner
REM Support:
REM     Student.csv
REM     Enrollment.csv
REM     Course.csv
REM
REM Usage:
REM     run_job2.cmd <job_name> <args>
REM
REM Example:
REM     run_job2.cmd students_by_course_and_score_range 251AI1 80 100
REM ============================================================


setlocal


REM ============================================================
REM Check Parameter
REM ============================================================

if "%1"=="" (

    echo Usage:
    echo run_job2.cmd ^<job_name^> [arguments]

    pause
    exit /b 1

)


set JOB_NAME=%1



REM ============================================================
REM Configuration
REM ============================================================

set HADOOP_HOME=D:\hadoop\hadoop-3.3.6
set JAVA_HOME=D:\Java11


set PYTHON=C:\Users\AdMin\AppData\Local\Python\pythoncore-3.14-64\python.exe


set PATH=%HADOOP_HOME%\bin;%JAVA_HOME%\bin;%PATH%



set PROJECT_ROOT=C:\Users\AdMin\BigDataTest



set JOB_DIR=%PROJECT_ROOT%\job\%JOB_NAME%



REM Local input

set STUDENT_FILE=%PROJECT_ROOT%\data\output\Student.csv
set ENROLLMENT_FILE=%PROJECT_ROOT%\data\output\Enrollment.csv
set COURSE_FILE=%PROJECT_ROOT%\data\output\Course.csv



REM HDFS input

set HDFS_INPUT=/input



set HDFS_OUTPUT=/output/%JOB_NAME%



set LOCAL_OUTPUT=%PROJECT_ROOT%\output\%JOB_NAME%



REM ============================================================
REM Check Job
REM ============================================================


if not exist "%JOB_DIR%\mapper.py" (

    echo mapper.py not found

    pause
    exit /b 1

)


if not exist "%JOB_DIR%\reducer.py" (

    echo reducer.py not found

    pause
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

    echo Export MongoDB failed

    pause
    exit /b 1

)



echo Export completed




REM ============================================================
REM Upload Multiple CSV To HDFS
REM ============================================================


echo.
echo ============================================================
echo Upload CSV To HDFS
echo ============================================================


echo Remove old input

call hdfs dfs -rm -r -f %HDFS_INPUT%



echo Create input folder

call hdfs dfs -mkdir %HDFS_INPUT%



echo Upload Student.csv

call hdfs dfs -put "%STUDENT_FILE%" %HDFS_INPUT%



echo Upload Enrollment.csv

call hdfs dfs -put "%ENROLLMENT_FILE%" %HDFS_INPUT%



echo Upload Course.csv

call hdfs dfs -put "%COURSE_FILE%" %HDFS_INPUT%



echo Verify input

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
echo Hadoop Streaming
echo ============================================================


cd /d "%JOB_DIR%"



hadoop jar "%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" ^
-file mapper.py ^
-file reducer.py ^
-file "%PROJECT_ROOT%\parser_1\csv_parser.py" ^
-input %HDFS_INPUT% ^
-output %HDFS_OUTPUT% ^
-mapper "%PYTHON% mapper.py" ^
-reducer "%PYTHON% reducer.py %2 %3 %4"



if errorlevel 1 (

    echo Hadoop Streaming failed

    cd /d "%PROJECT_ROOT%"

    pause

    exit /b 1

)



REM Remove copied parser

if exist "csv_parser.py" (

    del /q "csv_parser.py"

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

    echo Result:
    echo.

    type "%LOCAL_OUTPUT%\part-00000"


) else (

    echo part-00000 not found

)



echo.
echo ============================================================
echo Finished
echo ============================================================



pause


endlocal