@echo off
chcp 65001 >nul
cls
echo ========================================
echo   데이터베이스 구조 분석
echo ========================================
echo.

REM Anaconda Python 찾기
set PYTHON_EXE=python

if exist "C:\Users\%USERNAME%\anaconda3\python.exe" (
    set PYTHON_EXE=C:\Users\%USERNAME%\anaconda3\python.exe
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set PYTHON_EXE=C:\ProgramData\Anaconda3\python.exe
)

"%PYTHON_EXE%" check_database.py
