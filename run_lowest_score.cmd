@echo off
REM Run lowest_score_per_course - Lowest score per course
cd /d "%~dp0"
call run.cmd job/job/lowest_score_per_course/mapper.py job/job/lowest_score_per_course/reducer.py data/processed/Enrollment.csv output/lowest_score
echo.
echo Output: output\lowest_score\part-00000
pause

