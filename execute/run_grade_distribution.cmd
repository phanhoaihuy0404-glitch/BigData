@echo off
REM Run grade_distribution - Grade distribution per course
cd /d "%~dp0"
call run.cmd job/job/grade_distribution/mapper.py job/job/grade_distribution/reducer.py data/processed/Enrollment.csv output/grade_distribution
echo.
echo Output: output\grade_distribution\part-00000
pause

