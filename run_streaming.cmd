@echo off
REM =============================================
REM Hadoop Streaming Runner for BigDataProject
REM =============================================
setlocal enabledelayedexpansion

REM ---- CONFIG ----
set HADOOP_HOME=C:\hadoop\hadoop-3.3.6
set JAVA_HOME=C:\PROGRA~1\Java\JRE18~1.0_4
set PYTHON=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
set PATH=%PATH%;%HADOOP_HOME%\bin;%JAVA_HOME%\bin

REM ---- PARAMETERS (with defaults) ----
set INPUT_FILE=%1
if "%INPUT_FILE%"=="" set INPUT_FILE=data/processed/Enrollment.csv

set OUTPUT_DIR=%2
if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=output/job_output

set MAPPER_SCRIPT=%3
if "%MAPPER_SCRIPT%"=="" set MAPPER_SCRIPT=job/job/semester_count/mapper.py

set REDUCER_SCRIPT=%4
if "%REDUCER_SCRIPT%"=="" set REDUCER_SCRIPT=job/job/semester_count/reducer.py

echo ============================================
echo Hadoop Streaming Job
echo ============================================
echo HADOOP_HOME  : %HADOOP_HOME%
echo JAVA_HOME    : %JAVA_HOME%
echo Input        : %INPUT_FILE%
echo Output       : %OUTPUT_DIR%
echo Mapper       : %MAPPER_SCRIPT%
echo Reducer      : %REDUCER_SCRIPT%
echo ============================================

REM Remove existing output directory
if exist %OUTPUT_DIR% (
    echo Removing existing output directory: %OUTPUT_DIR%
    rmdir /s /q %OUTPUT_DIR%
)

REM Run Hadoop Streaming
%HADOOP_HOME%\bin\hadoop.cmd jar ^
    %HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar ^
    -D mapreduce.framework.name=local ^
    -file %MAPPER_SCRIPT% ^
    -file %REDUCER_SCRIPT% ^
    -input %INPUT_FILE% ^
    -output %OUTPUT_DIR% ^
    -mapper "%PYTHON% %MAPPER_SCRIPT%" ^
    -reducer "%PYTHON% %REDUCER_SCRIPT%"

echo ============================================
echo Job completed! Output saved to %OUTPUT_DIR%
echo ============================================

endlocal

