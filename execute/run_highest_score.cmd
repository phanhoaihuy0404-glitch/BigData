@echo off
REM Run highest_score - Highest score per course
cd /d "%~dp0"
call run.cmd job/job/highest_score/mapper.py job/job/highest_score/reducer.py data/processed/Enrollment.csv output/highest_score
echo.
echo Output: output\highest_score\part-00000
pause

