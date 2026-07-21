@echo off
REM =============================================
REM Run Hadoop Streaming Job - Quick launcher
REM =============================================
REM Usage: run.cmd [mapper] [reducer] [input] [output]
REM
REM Examples:
REM   run.cmd                          (default: semester_count)
REM   run.cmd job/job/semester_count/mapper.py job/job/semester_count/reducer.py
REM   run.cmd job/job/avg_midterm_per_course/mapper.py job/job/avg_midterm_per_course/reducer.py
REM =============================================

set HADOOP_HOME=C:\hadoop\hadoop-3.3.6
set JAVA_HOME=C:\PROGRA~1\Java\JRE18~1.0_4
set PYTHON=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe

set MAPPER=%1
set REDUCER=%2
set INPUT=%3
set OUTPUT=%4

if "%MAPPER%"=="" set MAPPER=job/job/semester_count/mapper.py
if "%REDUCER%"=="" set REDUCER=job/job/semester_count/reducer.py
if "%INPUT%"=="" set INPUT=data/processed/Enrollment.csv
if "%OUTPUT%"=="" set OUTPUT=output/job_output

echo ============================================
echo Hadoop Streaming - Quick Run
echo ============================================
echo Mapper : %MAPPER%
echo Reducer: %REDUCER%
echo Input  : %INPUT%
echo Output : %OUTPUT%
echo ============================================

REM Remove output directory if exists
if exist "%OUTPUT%" (
    rmdir /s /q "%OUTPUT%" 2>nul
)

REM Run Hadoop Streaming
"%HADOOP_HOME%\bin\hadoop.cmd" jar ^
    "%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar" ^
    -D mapreduce.framework.name=local ^
    -file "%MAPPER%" ^
    -file "%REDUCER%" ^
    -input "%INPUT%" ^
    -output "%OUTPUT%" ^
    -mapper "%PYTHON% %MAPPER%" ^
    -reducer "%PYTHON% %REDUCER%"

echo ============================================
if exist "%OUTPUT%\part-00000" (
    type "%OUTPUT%\part-00000"
)
echo ============================================
