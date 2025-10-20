@echo off
chcp 65001 >nul
cls
echo ========================================
echo   FastAPI 어선 항적 시각화
echo ========================================
echo.

echo [1/2] 패키지 설치 중...
pip install fastapi uvicorn pandas pydantic --quiet

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 패키지 설치 실패!
    echo.
    echo 해결방법:
    echo 1. Python이 설치되어 있는지 확인
    echo 2. 관리자 권한으로 실행
    echo 3. 수동 설치: pip install fastapi uvicorn pandas pydantic
    echo.
    pause
    exit /b
)

echo ✅ 패키지 설치 완료!
echo.

echo [2/2] 서버 시작 중...
echo.
echo 서버 주소: http://localhost:8080
echo 종료하려면 Ctrl+C를 누르세요
echo.
echo ========================================
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 서버 시작 실패!
    echo.
    echo INSTALL.md 파일을 참고하세요.
    echo.
    pause
)
