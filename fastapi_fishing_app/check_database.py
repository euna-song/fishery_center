"""
데이터베이스 구조 및 데이터 확인 도구
"""
import sqlite3
import os

db_path = r"C:\Users\User\Desktop\fishing_trajectory.db"

print("=" * 60)
print("데이터베이스 분석")
print("=" * 60)
print()

# 1. 파일 존재 확인
print(f"📁 경로: {db_path}")
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"✅ 파일 존재 ({size:,} bytes)")
else:
    print(f"❌ 파일 없음!")
    input("\n아무 키나 눌러 종료...")
    exit(1)

print()

# 2. 데이터베이스 연결
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("✅ 데이터베이스 연결 성공")
except Exception as e:
    print(f"❌ 연결 실패: {e}")
    input("\n아무 키나 눌러 종료...")
    exit(1)

print()
print("=" * 60)

# 3. 테이블 목록
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"📊 테이블 개수: {len(tables)}")
print()

for table in tables:
    table_name = table[0]
    print(f"📋 테이블: {table_name}")

    # 컬럼 정보
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"   컬럼 ({len(columns)}개):")
    for col in columns:
        print(f"      - {col[1]} ({col[2]})")

    # 데이터 개수
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"   📈 레코드 수: {count:,}개")

    # 샘플 데이터 (첫 3개)
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        samples = cursor.fetchall()
        print(f"   🔍 샘플 데이터:")
        for i, sample in enumerate(samples, 1):
            print(f"      {i}. {sample}")

    # 날짜 범위 확인 (datetime 컬럼이 있는 경우)
    if any('datetime' in col[1].lower() for col in columns):
        try:
            cursor.execute(f"SELECT MIN(datetime), MAX(datetime) FROM {table_name}")
            min_dt, max_dt = cursor.fetchone()
            print(f"   📅 날짜 범위: {min_dt} ~ {max_dt}")
        except:
            pass

    # MMSI 개수 확인
    if any('mmsi' in col[1].lower() for col in columns):
        try:
            cursor.execute(f"SELECT COUNT(DISTINCT mmsi) FROM {table_name}")
            mmsi_count = cursor.fetchone()[0]
            print(f"   🚢 고유 MMSI: {mmsi_count:,}개")
        except:
            pass

    # Status 분포 확인
    if any('status' in col[1].lower() for col in columns):
        try:
            cursor.execute(f"SELECT status, COUNT(*) FROM {table_name} GROUP BY status")
            status_dist = cursor.fetchall()
            print(f"   📊 Status 분포:")
            for status, cnt in status_dist:
                status_name = "조업" if status == 1 else "비조업" if status == 2 else f"기타({status})"
                print(f"      - {status_name}: {cnt:,}개")
        except:
            pass

    print()

print("=" * 60)
print()

# 4. 권장 설정
print("💡 FastAPI 앱 설정 정보:")
print()
if tables:
    first_table = tables[0][0]
    print(f"✅ 테이블명: {first_table}")
    print(f"✅ DB 경로: {db_path}")
    print()
    print("main.py에서 확인할 부분:")
    print(f'   DB_PATH = r"{db_path}"')
else:
    print("❌ 테이블이 없습니다!")

conn.close()
print()
print("=" * 60)
input("\n분석 완료! 아무 키나 눌러 종료...")
