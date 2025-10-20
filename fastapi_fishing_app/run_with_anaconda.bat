@echo off
chcp 65001 >nul
cls
echo ========================================
echo   Anaconda 환경에서 FastAPI 실행
echo ========================================
echo.

REM Anaconda 경로 찾기
set ANACONDA_PATH=

if exist "C:\Users\%USERNAME%\anaconda3\python.exe" (
    set ANACONDA_PATH=C:\Users\%USERNAME%\anaconda3
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set ANACONDA_PATH=C:\ProgramData\Anaconda3
) else if exist "C:\Users\%USERNAME%\AppData\Local\Continuum\anaconda3\python.exe" (
    set ANACONDA_PATH=C:\Users\%USERNAME%\AppData\Local\Continuum\anaconda3
) else if exist "C:\Anaconda3\python.exe" (
    set ANACONDA_PATH=C:\Anaconda3
)

if "%ANACONDA_PATH%"=="" (
    echo ❌ Anaconda를 찾을 수 없습니다!
    echo.
    echo 다음 방법을 시도하세요:
    echo 1. Anaconda Prompt를 열어서 실행
    echo 2. START_HERE.txt 파일 참고
    echo.
    pause
    exit /b
)

echo ✅ Anaconda 발견: %ANACONDA_PATH%
echo.

REM Anaconda 환경 활성화
call "%ANACONDA_PATH%\Scripts\activate.bat" 2>nul

echo [1/2] 패키지 설치 중...
"%ANACONDA_PATH%\Scripts\pip.exe" install fastapi uvicorn pandas pydantic --quiet

if %ERRORLEVEL% NEQ 0 (
    echo ❌ 패키지 설치 실패
    echo Anaconda Prompt에서 수동으로 실행해주세요.
    pause
    exit /b
)

echo ✅ 패키지 설치 완료!
echo.

echo [2/2] 서버 시작 중...
echo.
echo 🌐 브라우저에서 http://localhost:8080 접속하세요
echo 🛑 종료하려면 Ctrl+C를 누르세요
echo.
echo ========================================
echo.

"%ANACONDA_PATH%\python.exe" main.py

pause
