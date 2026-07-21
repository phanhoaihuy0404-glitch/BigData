@echo off
REM Run count_course - Count students per course
cd /d "%~dp0"
call run.cmd job/job/count_course/mapper.py job/job/count_course/reducer.py data/processed/Enrollment.csv output/count_course
echo.
echo Output: output\count_course\part-00000
pause

