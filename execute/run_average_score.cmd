@echo off
REM Run average_score - Average score per course
cd /d "%~dp0"
call run.cmd job/job/average_score/mapper.py job/job/average_score/reducer.py data/processed/Enrollment.csv output/average_score
echo.
echo Output: output\average_score\part-00000
pause

