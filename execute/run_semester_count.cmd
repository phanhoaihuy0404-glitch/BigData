@echo off
REM Run semester_count - Count students per semester
cd /d "%~dp0"
call run.cmd job/job/semester_count/mapper.py job/job/semester_count/reducer.py data/processed/Enrollment.csv output/semester_count
echo.
echo Output: output\semester_count\part-00000
pause

