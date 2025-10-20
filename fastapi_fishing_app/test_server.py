"""
간단한 테스트 서버 - 의존성 확인
"""
import sys

print("Python version:", sys.version)
print("\nChecking dependencies...")

try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError:
    print("❌ FastAPI not installed")
    print("   Run: pip install fastapi")

try:
    import uvicorn
    print(f"✅ Uvicorn: {uvicorn.__version__}")
except ImportError:
    print("❌ Uvicorn not installed")
    print("   Run: pip install uvicorn")

try:
    import pandas
    print(f"✅ Pandas: {pandas.__version__}")
except ImportError:
    print("❌ Pandas not installed")
    print("   Run: pip install pandas")

try:
    import pydantic
    print(f"✅ Pydantic: {pydantic.__version__}")
except ImportError:
    print("❌ Pydantic not installed")
    print("   Run: pip install pydantic")

import os
db_path = r"C:\Users\User\Desktop\fishing_trajectory.db"
print(f"\n데이터베이스 파일 확인:")
if os.path.exists(db_path):
    print(f"✅ 파일 존재: {db_path}")
    file_size = os.path.getsize(db_path)
    print(f"   크기: {file_size:,} bytes")
else:
    print(f"❌ 파일 없음: {db_path}")

print("\n모든 확인 완료!")
