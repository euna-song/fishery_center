@echo off
echo ========================================
echo   FastAPI 설치 및 실행
echo ========================================
echo.

REM Anaconda 환경 확인
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Anaconda를 찾을 수 없습니다.
    echo Anaconda Prompt에서 이 스크립트를 실행해주세요.
    echo.
    echo 또는 수동으로 다음 명령어를 실행하세요:
    echo   conda install -c conda-forge fastapi uvicorn pandas
    echo   python main.py
    pause
    exit /b
)

echo [1/3] Conda 환경 확인 중...
conda --version

echo.
echo [2/3] 필요한 패키지 설치 중...
conda install -y -c conda-forge fastapi uvicorn pandas pydantic

if %ERRORLEVEL% NEQ 0 (
    echo 패키지 설치 실패! pip로 재시도합니다...
    pip install fastapi uvicorn pandas pydantic
)

echo.
echo [3/3] FastAPI 서버 시작...
echo 브라우저에서 http://localhost:8080 으로 접속하세요
echo.
python main.py

pause
