@echo off
REM =============================================
REM Run ALL Hadoop Streaming Jobs
REM =============================================
setlocal enabledelayedexpansion

echo ============================================
echo Hadoop Streaming - RUN ALL JOBS
echo ============================================
echo.
echo This will run ALL 10 MapReduce jobs sequentially
echo.

set JOBS=semester_count count_course highest_score average_score grade_distribution pass_fail_per_course lowest_score_per_course avg_midterm_per_course course_performance_analytics top_n_course

set COUNT=1
for %%j in (%JOBS%) do (
    echo ============================================
    echo [%COUNT%/10] Running %%j ...
    echo ============================================
    call run_job.cmd %%j
    echo.
    set /a COUNT+=1
)

echo ============================================
echo ALL 10 JOBS COMPLETED!
echo ============================================
echo.
echo Check results in:
for %%j in (%JOBS%) do (
    if exist "C:\Users\AdMin\BigDataTest\output\%%j\part-00000" (
        echo   [OK] output\%%j\part-00000
    ) else (
        echo   [FAIL] output\%%j\ - not found!
    )
)
echo.

endlocal
pause
