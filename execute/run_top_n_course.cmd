@echo off
REM Run top_n_course - Top N courses by enrollment
cd /d "%~dp0"
call run.cmd job/job/top_n_course/mapper.py job/job/top_n_course/reducer.py data/processed/Enrollment.csv output/top_n_course
echo.
echo Output: output\top_n_course\part-00000
pause

