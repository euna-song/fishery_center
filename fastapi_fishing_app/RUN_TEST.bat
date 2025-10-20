@echo off
chcp 65001 >nul
cls
echo ========================================
echo   FastAPI 테스트 서버
echo ========================================
echo.
echo 이 스크립트는 서버가 정상 작동하는지 확인합니다.
echo.

REM Anaconda 경로 찾기
set PYTHON_EXE=python

if exist "C:\Users\%USERNAME%\anaconda3\python.exe" (
    set PYTHON_EXE=C:\Users\%USERNAME%\anaconda3\python.exe
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set PYTHON_EXE=C:\ProgramData\Anaconda3\python.exe
)

echo Python 경로: %PYTHON_EXE%
echo.

"%PYTHON_EXE%" test_simple.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo 오류가 발생했습니다!
    echo ========================================
    echo.
    echo Anaconda Prompt를 열고 다음을 실행하세요:
    echo.
    echo   cd C:\Users\User\fishery_center\fastapi_fishing_app
    echo   pip install fastapi uvicorn pandas pydantic
    echo   python test_simple.py
    echo.
)

pause
