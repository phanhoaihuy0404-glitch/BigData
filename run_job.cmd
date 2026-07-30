@echo off
REM ============================================================
REM Hadoop Streaming Job Runner (HDFS Version)
REM Usage:
REM     run_job.cmd <job_name>
REM ============================================================

setlocal


REM ============================================================
REM Check Parameter
REM ============================================================

if "%1"=="" (
    echo Usage: run_job.cmd ^<job_name^>
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
    pause
    exit /b 1
)


if not exist "%JOB_DIR%\reducer.py" (
    echo.
    echo [FAIL] reducer.py not found
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
    echo.
    echo [FAIL] MongoDB export failed
    pause
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
    pause
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


call hdfs dfs -rm -r -f %HDFS_OUTPUT%


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
echo.



REM Move into job directory
cd /d "%JOB_DIR%"


echo Current directory:
cd



hadoop jar "%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" ^
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

    pause
    exit /b 1
)



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
    pause
    exit /b 1
)




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

    echo [FAIL] part-00000 not found

)



echo.
echo ============================================================
echo Finished
echo ============================================================



pause

endlocal