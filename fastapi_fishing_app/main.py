"""
FastAPI 어선 항적 시각화 애플리케이션
Streamlit에서 FastAPI로 변환
데이터베이스: C:\Users\User\Desktop\fishing_trajectory.db
사용자 요청: streamlit 말고 fastAPI로 만들고 싶어. 데이터는 C:\Users\User\Desktop\fishing_trafectory.db에서 가져올거야
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, date
import sqlite3
import pandas as pd
from pydantic import BaseModel
import os

app = FastAPI(
    title="🚢 어선 항적 시각화 API",
    description="FastAPI 기반 어선 항적 데이터 시각화 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 설정
DB_PATH = r"C:\Users\User\Desktop\fishing_trajectory.db"
TILE_URL = "http://127.0.0.1:8000/tiles/{z}/{x}/{y}.png"  # MBTiles 타일 서버
INITIAL_ZOOM = 7
MAX_ZOOM = 18

# Pydantic 모델
class TrajectoryPoint(BaseModel):
    mmsi: str
    datetime: str
    lat: float
    lon: float
    status: int
    status_name: str

class MMSIInfo(BaseModel):
    mmsi: str
    count: int

class DataRequest(BaseModel):
    start_date: str
    end_date: str
    start_hour: int = 0
    end_hour: int = 23
    mmsi_list: Optional[List[str]] = None
    status_list: Optional[List[int]] = [1, 2]
    sampling_step: int = 5

# 데이터베이스 연결
def connect_db():
    """SQLite 데이터베이스 연결"""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail=f"데이터베이스 파일을 찾을 수 없습니다: {DB_PATH}")
    return sqlite3.connect(DB_PATH, timeout=30)

@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지 - 인터랙티브 지도 UI"""
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/health")
async def health_check():
    """헬스 체크 - DB 연결 상태 확인"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
        tables = cursor.fetchall()
        conn.close()
        return {
            "status": "healthy",
            "database": "connected",
            "db_path": DB_PATH,
            "tables_found": len(tables)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 연결 실패: {str(e)}")

@app.get("/api/tables")
async def get_tables():
    """데이터베이스 테이블 목록 조회"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"테이블 조회 실패: {str(e)}")

@app.get("/api/mmsi", response_model=List[MMSIInfo])
async def get_mmsi_list(
    start_date: str = Query(..., description="시작 날짜 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="종료 날짜 (YYYY-MM-DD)"),
    start_hour: int = Query(0, ge=0, le=23),
    end_hour: int = Query(23, ge=0, le=23),
    limit: int = Query(100, description="최대 MMSI 개수")
):
    """지정된 기간의 MMSI 목록 조회"""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # 테이블 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
        table_name = cursor.fetchone()[0]

        start_datetime = f"{start_date} {start_hour:02d}:00:00"
        end_datetime = f"{end_date} {end_hour:02d}:59:59"

        query = f"""
            SELECT mmsi, COUNT(*) as count
            FROM {table_name}
            WHERE datetime >= ? AND datetime <= ?
            GROUP BY mmsi
            ORDER BY count DESC
            LIMIT ?
        """

        df = pd.read_sql_query(query, conn, params=[start_datetime, end_datetime, limit])
        conn.close()

        result = [{"mmsi": str(row['mmsi']), "count": int(row['count'])} for _, row in df.iterrows()]
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MMSI 조회 실패: {str(e)}")

@app.post("/api/trajectory", response_model=List[TrajectoryPoint])
async def get_trajectory_data(request: DataRequest):
    """항적 데이터 조회"""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # 테이블 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
        table_name = cursor.fetchone()[0]

        start_datetime = f"{request.start_date} {request.start_hour:02d}:00:00"
        end_datetime = f"{request.end_date} {request.end_hour:02d}:59:59"

        # MMSI 필터
        mmsi_filter = ""
        params = [start_datetime, end_datetime]

        if request.mmsi_list:
            placeholders = ','.join(['?'] * len(request.mmsi_list))
            mmsi_filter = f"AND mmsi IN ({placeholders})"
            params.extend(request.mmsi_list)

        # Status 필터
        status_placeholders = ','.join(['?'] * len(request.status_list))
        params.extend(request.status_list)

        query = f"""
            SELECT mmsi, datetime, lat, lon, status,
                   ROW_NUMBER() OVER (PARTITION BY mmsi ORDER BY datetime) as rn
            FROM {table_name}
            WHERE datetime >= ? AND datetime <= ?
            {mmsi_filter}
            AND status IN ({status_placeholders})
            ORDER BY mmsi, datetime
        """

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # 샘플링
        if not df.empty:
            df_sampled = df[df['rn'] % request.sampling_step == 1].copy()
            df_sampled['status_name'] = df_sampled['status'].apply(lambda s: '조업' if s == 1 else '비조업')

            result = []
            for _, row in df_sampled.iterrows():
                result.append({
                    "mmsi": str(row['mmsi']),
                    "datetime": str(row['datetime']),
                    "lat": float(row['lat']),
                    "lon": float(row['lon']),
                    "status": int(row['status']),
                    "status_name": row['status_name']
                })

            return result

        return []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"항적 데이터 조회 실패: {str(e)}")

@app.get("/api/stats")
async def get_statistics(
    start_date: str,
    end_date: str,
    start_hour: int = 0,
    end_hour: int = 23
):
    """데이터 통계 정보"""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # 테이블 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
        table_name = cursor.fetchone()[0]

        start_datetime = f"{start_date} {start_hour:02d}:00:00"
        end_datetime = f"{end_date} {end_hour:02d}:59:59"

        query = f"""
            SELECT
                COUNT(*) as total_count,
                COUNT(DISTINCT mmsi) as unique_vessels,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as fishing_count,
                SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) as non_fishing_count,
                MIN(datetime) as min_datetime,
                MAX(datetime) as max_datetime
            FROM {table_name}
            WHERE datetime >= ? AND datetime <= ?
        """

        cursor.execute(query, [start_datetime, end_datetime])
        result = cursor.fetchone()
        conn.close()

        return {
            "total_count": result[0],
            "unique_vessels": result[1],
            "fishing_count": result[2],
            "non_fishing_count": result[3],
            "min_datetime": result[4],
            "max_datetime": result[5]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
