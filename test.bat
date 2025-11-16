@echo off
REM ============================================================================
REM spacetime-playground Test Runner for Windows
REM ============================================================================

echo.
echo ========================================================================
echo   SPACETIME-PLAYGROUND PRE-RELEASE TEST
echo ========================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo Running comprehensive test suite...
echo.

REM Run the test script
python test_before_release.py

echo.
echo ========================================================================
echo Test complete!
echo ========================================================================
echo.

pause
