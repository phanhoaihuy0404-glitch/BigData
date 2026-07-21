@echo off
REM Run avg_midterm_per_course - Average midterm score per course
cd /d "%~dp0"
call run.cmd job/job/avg_midterm_per_course/mapper.py job/job/avg_midterm_per_course/reducer.py data/processed/Enrollment.csv output/avg_midterm
echo.
echo Output: output\avg_midterm\part-00000
pause

