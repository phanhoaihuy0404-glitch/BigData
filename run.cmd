@echo off
REM =============================================
REM Run Hadoop Streaming Job - Quick launcher
REM =============================================
REM Usage: run.cmd [mapper] [reducer] [input] [output]
REM
REM Examples:
REM   run.cmd                          (default: semester_count)
REM   run.cmd mapper/semester_count.py reducer/semester_count.py
REM   run.cmd mapper/avg_midterm_per_course.py reducer/avg_midterm_per_course.py
REM =============================================

set HADOOP_HOME=C:\hadoop\hadoop-3.3.6
set JAVA_HOME=C:\PROGRA~1\Java\JRE18~1.0_4

set MAPPER=%1
set REDUCER=%2
set INPUT=%3
set OUTPUT=%4

if "%MAPPER%"=="" set MAPPER=mapper/semester_count.py
if "%REDUCER%"=="" set REDUCER=reducer/semester_count.py
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
    -mapper "python %MAPPER%" ^
    -reducer "python %REDUCER%"

echo ============================================
if exist "%OUTPUT%\part-00000" (
    type "%OUTPUT%\part-00000"
)
echo ============================================
