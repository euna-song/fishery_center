@echo off
chcp 65001 >nul
cls
echo ========================================
echo   🚢 어선 항적 시각화 시스템
echo ========================================
echo.

REM Anaconda Python 찾기
set PYTHON_EXE=python

if exist "C:\Users\%USERNAME%\anaconda3\python.exe" (
    set PYTHON_EXE=C:\Users\%USERNAME%\anaconda3\python.exe
    echo ✅ Anaconda Python 찾음
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set PYTHON_EXE=C:\ProgramData\Anaconda3\python.exe
    echo ✅ Anaconda Python 찾음
) else (
    echo ℹ️  기본 Python 사용
)

echo.
echo 🚀 메인 애플리케이션 시작 중...
echo.
echo 📍 서버 주소: http://localhost:8888
echo 🛑 종료하려면: Ctrl+C
echo.
echo ========================================
echo.

"%PYTHON_EXE%" main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 서버 시작 실패!
    echo.
    echo 가능한 원인:
    echo 1. 데이터베이스 파일을 찾을 수 없음
    echo 2. 포트 8080이 이미 사용 중
    echo 3. 패키지 오류
    echo.
    echo INSTALL.md 파일을 참고하세요.
    echo.
)

pause
