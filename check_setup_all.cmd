@echo off
echo ============================================
echo   CHECK ALL SETUP - BigDataTest Machine
echo ============================================
echo.

:: ---- CHECK JAVA ----
echo [1/6] Check Java...
java -version 2>&1
echo.
echo JAVA_HOME: %JAVA_HOME%
echo.

:: ---- CHECK HADOOP ----
echo [2/6] Check Hadoop...
hadoop version 2>&1
echo.
echo HADOOP_HOME: %HADOOP_HOME%
echo.

:: ---- CHECK STREAMING JAR ----
echo [3/6] Check Streaming JAR...
dir D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar 2>nul
if exist D:\hadoop\hadoop-3.3.6\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar (
    echo   [OK] Streaming JAR found
) else (
    echo   [FAIL] Streaming JAR not found
)
echo.

:: ---- CHECK PYTHON ----
echo [4/6] Check Python...
py --list
echo.
py -3.14 -c "import sys;print(sys.executable)"
echo.

:: ---- CHECK PARSER IMPORT ----
echo [5/6] Check parser_1 import...
set PYTHONPATH=C:\Users\AdMin\BigDataTest
py -3.14 C:\Users\AdMin\BigDataTest\test_import.py 2>&1
if %ERRORLEVEL% equ 0 (echo   [OK]) else (echo   [FAIL])
echo.

:: ---- CHECK ENROLLMENT DATA ----
echo [6/6] Check Enrollment data...
more C:\Users\AdMin\BigDataTest\data\processed\Enrollment.csv
echo.

echo ============================================
echo   ALL CHECKS COMPLETE
echo ============================================
pause
