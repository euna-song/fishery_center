"""
간단한 FastAPI 테스트 서버
데이터베이스 연결 없이 기본 동작만 확인
"""

print("=" * 50)
print("FastAPI 테스트 서버 시작")
print("=" * 50)
print()

# 1. Python 버전 확인
import sys
print(f"✅ Python 버전: {sys.version}")
print()

# 2. 필수 패키지 확인
required_packages = ['fastapi', 'uvicorn', 'pydantic']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"✅ {package} 설치됨")
    except ImportError:
        print(f"❌ {package} 없음")
        missing_packages.append(package)

print()

if missing_packages:
    print("⚠️  다음 패키지를 설치해주세요:")
    print(f"   pip install {' '.join(missing_packages)}")
    input("\n아무 키나 눌러 종료...")
    sys.exit(1)

# 3. 데이터베이스 파일 확인
import os
db_path = r"C:\Users\User\Desktop\fishing_trajectory.db"
print(f"데이터베이스 경로: {db_path}")
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"✅ 데이터베이스 파일 존재 ({size:,} bytes)")
else:
    print(f"⚠️  데이터베이스 파일 없음 (서버는 실행되지만 데이터 조회 불가)")

print()
print("=" * 50)
print("간단한 테스트 서버를 시작합니다...")
print("=" * 50)
print()

# 4. 간단한 FastAPI 서버 실행
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>FastAPI 테스트 성공!</title>
        <style>
            body {
                font-family: Arial;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f0f0f0;
            }
            .success {
                background: #4caf50;
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
            }
            h1 { margin: 0; }
            .info {
                background: white;
                padding: 20px;
                margin-top: 20px;
                border-radius: 10px;
            }
            .next-step {
                background: #2196F3;
                color: white;
                padding: 15px;
                margin-top: 20px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="success">
            <h1>✅ FastAPI 서버가 정상 작동합니다!</h1>
            <p style="font-size: 18px; margin-top: 20px;">
                이제 메인 애플리케이션을 실행할 수 있습니다.
            </p>
        </div>

        <div class="info">
            <h2>📋 확인 완료</h2>
            <ul>
                <li>✅ Python 설치됨</li>
                <li>✅ FastAPI 설치됨</li>
                <li>✅ Uvicorn 설치됨</li>
                <li>✅ 서버 실행 성공</li>
            </ul>
        </div>

        <div class="next-step">
            <h2>🚀 다음 단계</h2>
            <p>테스트가 성공했으니 이제 메인 애플리케이션을 실행하세요:</p>
            <ol>
                <li>현재 서버를 종료 (Ctrl+C)</li>
                <li>다음 명령어 실행: <code>python main.py</code></li>
                <li>브라우저에서 http://localhost:8080 접속</li>
            </ol>
        </div>
    </body>
    </html>
    """

@app.get("/api/test")
def test_api():
    return {
        "status": "success",
        "message": "API 작동 중!",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    print("🌐 브라우저에서 http://localhost:8080 을 열어주세요")
    print("🛑 종료하려면 Ctrl+C 를 누르세요")
    print()

    try:
        uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
    except Exception as e:
        print(f"\n❌ 서버 시작 실패: {e}")
        input("\n아무 키나 눌러 종료...")
