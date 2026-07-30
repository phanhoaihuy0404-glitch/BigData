@echo off
REM ============================================================================
REM  run_all.cmd - Local MapReduce Simulation Runner
REM
REM  Simulates Hadoop Streaming pipeline:
REM    stdin -> Mapper -> stdout -> Python sort -> Reducer -> output file
REM
REM  Uses Python-based sort instead of Windows sort.exe to avoid
REM  "Not enough main memory to complete the sort" errors.
REM
REM  When Hadoop Streaming is fixed, simply replace the pipeline with:
REM    hadoop jar ... -mapper "python mapper.py" -reducer "python reducer.py"
REM
REM  Usage: Run from the project root:
REM    job\run_all.cmd
REM ============================================================================

setlocal enabledelayedexpansion

REM ----- Configuration -----
set PYTHON=C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
set PROJECT_ROOT=C:\Users\Admin\Desktop\BigData\BigDataProject
set INPUT_FILE=%PROJECT_ROOT%\data\processed\Enrollment.csv
set OUTPUT_DIR=%PROJECT_ROOT%\data\output
set JOB_DIR=%PROJECT_ROOT%\job\job
set SORT_CMD="%PYTHON%" "%JOB_DIR%\sort.py"

REM Set PYTHONPATH so mappers can find "parser.enrollment_parser"
set PYTHONPATH=%PROJECT_ROOT%

REM ----- Ensure output directory exists -----
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo ===================================================
echo  Hadoop MapReduce Local Simulation (Windows)
echo ===================================================
echo.

REM ============================================================================
REM  JOB 1: semester_count - Count students per semester
echo [1/10] Running semester_count ...
cd /d "%JOB_DIR%\semester_count"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\semester_count.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] semester_count completed
) else (
    echo   [FAIL] semester_count failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 2: count_course - Count students per course
echo [2/10] Running count_course ...
cd /d "%JOB_DIR%\count_course"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\count_course.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] count_course completed
) else (
    echo   [FAIL] count_course failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 3: average_score - Average score per course
echo [3/10] Running average_score ...
cd /d "%JOB_DIR%\average_score"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\average_score.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] average_score completed
) else (
    echo   [FAIL] average_score failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 4: grade_distribution - Grade distribution per course
echo [4/10] Running grade_distribution ...
cd /d "%JOB_DIR%\grade_distribution"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\grade_distribution.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] grade_distribution completed
) else (
    echo   [FAIL] grade_distribution failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 5: highest_score - Highest score per course
echo [5/10] Running highest_score ...
cd /d "%JOB_DIR%\highest_score"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\highest_score.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] highest_score completed
) else (
    echo   [FAIL] highest_score failed
)
cd /d "%JOB_DIR%"
echo.


REM ============================================================================
REM  JOB 6: top_n_course - Top N courses by enrollment

echo [6/10] Running top_n_course ...

cd /d "%JOB_DIR%\top_n_course"

"%PYTHON%" find_top_n.py ^
"%OUTPUT_DIR%\count_course" ^
"%OUTPUT_DIR%\top_n_course_top10.txt"

if %ERRORLEVEL% equ 0 (
    echo   [OK] Top N extracted
) else (
    echo   [FAIL] top_n_course failed
)

cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 7: avg_midterm_per_course - Average midterm score per course
echo [7/10] Running avg_midterm_per_course ...
cd /d "%JOB_DIR%\avg_midterm_per_course"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\avg_midterm_per_course.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] avg_midterm_per_course completed
) else (
    echo   [FAIL] avg_midterm_per_course failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 8: course_performance_analytics - Course performance multi-metrics
echo [8/10] Running course_performance_analytics ...
cd /d "%JOB_DIR%\course_performance_analytics"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\course_performance_analytics.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] course_performance_analytics completed
) else (
    echo   [FAIL] course_performance_analytics failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 9: lowest_score_per_course - Lowest score per course
echo [9/10] Running lowest_score_per_course ...
cd /d "%JOB_DIR%\lowest_score_per_course"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\lowest_score_per_course.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] lowest_score_per_course completed
) else (
    echo   [FAIL] lowest_score_per_course failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  JOB 10: pass_fail_per_course - Pass/Fail statistics per course
echo [10/10] Running pass_fail_per_course ...
cd /d "%JOB_DIR%\pass_fail_per_course"
type "%INPUT_FILE%" | "%PYTHON%" mapper.py 2>nul | %SORT_CMD% | "%PYTHON%" reducer.py > "%OUTPUT_DIR%\pass_fail_per_course.txt"
if %ERRORLEVEL% equ 0 (
    echo   [OK] pass_fail_per_course completed
) else (
    echo   [FAIL] pass_fail_per_course failed
)
cd /d "%JOB_DIR%"
echo.

REM ============================================================================
REM  Summary
echo ===================================================
echo  All jobs completed!
echo  Output files are in: %OUTPUT_DIR%
echo ===================================================
echo.
dir /b "%OUTPUT_DIR%\*.txt" 2>nul
echo.
echo  Next Step: When Hadoop Streaming is fixed, run:
echo    run_streaming.cmd
echo ===================================================

endlocal
pause

