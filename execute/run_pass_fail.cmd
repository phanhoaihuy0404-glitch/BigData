@echo off
REM Run pass_fail_per_course - Pass/Fail statistics per course
cd /d "%~dp0"
call run.cmd job/job/pass_fail_per_course/mapper.py job/job/pass_fail_per_course/reducer.py data/processed/Enrollment.csv output/pass_fail
echo.
echo Output: output\pass_fail\part-00000
pause

