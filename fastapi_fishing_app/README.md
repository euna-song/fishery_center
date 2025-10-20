# 🚢 FastAPI 어선 항적 시각화 시스템

Streamlit에서 FastAPI로 변환한 어선 항적 데이터 시각화 애플리케이션

## 📁 프로젝트 구조

```
fastapi_fishing_app/
├── main.py                 # FastAPI 메인 애플리케이션
├── templates/
│   └── index.html          # 프론트엔드 UI
├── requirements.txt        # Python 의존성
└── README.md              # 문서
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. 브라우저에서 접속

```
http://localhost:8080
```

## 📊 데이터 소스

- **데이터베이스**: `C:\Users\User\Desktop\fishing_trajectory.db`
- **필드**: mmsi, datetime, lat, lon, status

## 🎯 API 엔드포인트

### 헬스 체크
```
GET /api/health
```

### 테이블 목록
```
GET /api/tables
```

### MMSI 목록 조회
```
GET /api/mmsi?start_date=2023-01-11&end_date=2023-01-15&start_hour=0&end_hour=23&limit=100
```

### 항적 데이터 조회
```
POST /api/trajectory
Content-Type: application/json

{
  "start_date": "2023-01-11",
  "end_date": "2023-01-15",
  "start_hour": 0,
  "end_hour": 23,
  "mmsi_list": ["123456789"],
  "status_list": [1, 2],
  "sampling_step": 5
}
```

### 통계 정보
```
GET /api/stats?start_date=2023-01-11&end_date=2023-01-15
```

## 🗺️ 기능

- ✅ 인터랙티브 지도 (Leaflet.js)
- ✅ 실시간 데이터 조회
- ✅ MMSI 기반 선박 필터링
- ✅ 조업/비조업 상태 시각화
- ✅ 데이터 샘플링 (성능 최적화)
- ✅ 항적 통계 표시
- ✅ RESTful API

## 🎮 사용 방법

1. **날짜 범위 설정**: 시작/종료 날짜 및 시간 선택
2. **MMSI 불러오기**: 해당 기간의 선박 목록 조회
3. **선박 선택**: 시각화할 선박 체크
4. **샘플링 설정**: 데이터 간격 조정 (1-20)
5. **시각화 실행**: 지도에 항적 표시

## 🔧 설정

### 데이터베이스 경로 변경

`main.py`에서 수정:
```python
DB_PATH = r"C:\Users\User\Desktop\fishing_trajectory.db"
```

### 포트 변경

```bash
uvicorn main:app --port 원하는포트번호
```

## 📝 원본 파일

- **Streamlit 버전**: `C:\Users\User\Desktop\streamlit_mbtiles9_re.py`
- **변환 날짜**: 2025-10-20
- **사용자 요청**: streamlit 말고 fastAPI로 만들고 싶어. 데이터는 C:\Users\User\Desktop\fishing_trafectory.db에서 가져올거야

## 🆚 Streamlit vs FastAPI 비교

| 기능 | Streamlit | FastAPI |
|------|-----------|---------|
| 프레임워크 | Streamlit | FastAPI + HTML/JS |
| API | ❌ | ✅ RESTful API |
| 커스터마이징 | 제한적 | 자유로움 |
| 성능 | 중간 | 높음 |
| 배포 | 쉬움 | 중간 |
| 프론트엔드 분리 | ❌ | ✅ |

## 📌 주요 개선사항

- 🔥 RESTful API로 프론트엔드와 백엔드 분리
- 🚀 더 빠른 응답 속도
- 🎨 커스텀 UI/UX 가능
- 📱 모바일 반응형 디자인
- 🔌 외부 서비스와 연동 가능

## 🐛 트러블슈팅

### 데이터베이스 연결 실패
- 데이터베이스 파일 경로 확인
- 파일 권한 확인

### 포트 충돌
- 다른 포트 사용: `--port 8081`

### CORS 에러
- `main.py`의 CORS 설정 확인

## 📄 라이선스

MIT License

## 👤 작성자

euna-song
