@echo off
REM Run course_performance_analytics - Course performance multi-metrics
cd /d "%~dp0"
call run.cmd job/job/course_performance_analytics/mapper.py job/job/course_performance_analytics/reducer.py data/processed/Enrollment.csv output/performance
echo.
echo Output: output\performance\part-00000
pause

