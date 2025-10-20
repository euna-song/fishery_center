# 🚀 설치 및 실행 가이드

## 문제: http://localhost:8080 실행 안됨

FastAPI 서버가 실행되지 않는 이유는 다음 중 하나입니다:

1. ❌ Python이 제대로 설치되지 않음
2. ❌ 필요한 패키지가 설치되지 않음
3. ❌ 서버가 실행되지 않음

## ✅ 해결 방법

### 1단계: Python 확인

명령 프롬프트(CMD)를 열고 다음 명령어를 실행하세요:

```cmd
python --version
```

또는

```cmd
python3 --version
```

**결과:**
- 성공: `Python 3.x.x` 출력됨 → 2단계로
- 실패: `'python'은(는) ... 인식할 수 없습니다` → Python 설치 필요

#### Python 설치 (필요한 경우)

1. https://www.python.org/downloads/ 방문
2. "Download Python 3.x" 클릭
3. 설치 시 **"Add Python to PATH"** 체크 필수!
4. 설치 후 CMD 재시작

### 2단계: 의존성 설치

명령 프롬프트에서 실행:

```cmd
cd C:\Users\User\fishery_center\fastapi_fishing_app
pip install fastapi uvicorn pandas pydantic
```

**또는** requirements.txt 사용:

```cmd
cd C:\Users\User\fishery_center\fastapi_fishing_app
pip install -r requirements.txt
```

### 3단계: 서버 실행

#### 방법 1: Python 직접 실행

```cmd
cd C:\Users\User\fishery_center\fastapi_fishing_app
python main.py
```

#### 방법 2: run.bat 실행

`run.bat` 파일을 더블클릭

#### 방법 3: uvicorn 직접 실행

```cmd
cd C:\Users\User\fishery_center\fastapi_fishing_app
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 4단계: 브라우저 접속

서버가 정상 실행되면 다음 메시지가 나타납니다:

```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

브라우저에서 접속:

```
http://localhost:8080
```

## 🔍 오류 해결

### 오류 1: "ModuleNotFoundError: No module named 'fastapi'"

**원인:** FastAPI가 설치되지 않음

**해결:**
```cmd
pip install fastapi
```

### 오류 2: "ModuleNotFoundError: No module named 'uvicorn'"

**원인:** Uvicorn이 설치되지 않음

**해결:**
```cmd
pip install uvicorn
```

### 오류 3: "Address already in use"

**원인:** 8080 포트가 이미 사용 중

**해결:** 다른 포트 사용
```cmd
python main.py --port 8081
```

또는

```cmd
uvicorn main:app --port 8081
```

그리고 브라우저에서 `http://localhost:8081` 접속

### 오류 4: "데이터베이스 파일을 찾을 수 없습니다"

**원인:** fishing_trajectory.db 파일 경로 오류

**해결:** main.py 파일 수정

```python
DB_PATH = r"C:\Users\User\Desktop\fishing_trajectory.db"
```

실제 데이터베이스 파일 위치로 변경

### 오류 5: Python이 "Python"만 출력하고 실행 안됨

**원인:** Windows Store Python 별칭 문제

**해결방법:**

1. Windows 설정 열기
2. "앱 및 기능" → "앱 실행 별칭"
3. "Python" 관련 항목을 모두 끄기
4. 실제 Python 설치 (python.org)

## 📋 빠른 체크리스트

- [ ] Python 설치됨 (`python --version` 확인)
- [ ] pip 작동함 (`pip --version` 확인)
- [ ] FastAPI 설치됨 (`pip show fastapi`)
- [ ] Uvicorn 설치됨 (`pip show uvicorn`)
- [ ] Pandas 설치됨 (`pip show pandas`)
- [ ] 데이터베이스 파일 존재 확인
- [ ] 8080 포트 사용 가능
- [ ] 서버 실행 중
- [ ] 브라우저에서 접속 가능

## 🎯 최소 요구사항

- **Python**: 3.8 이상
- **메모리**: 최소 2GB RAM
- **디스크**: 500MB 여유 공간
- **OS**: Windows 10/11

## 📞 추가 도움

모든 방법을 시도했는데도 안 되면:

1. `standalone.html` 파일을 브라우저에서 열어서 설치 가이드 확인
2. 명령 프롬프트 출력 오류 메시지 확인
3. 로그 파일 확인

## ✨ 성공 확인

서버가 정상 실행되면:

1. 명령 프롬프트에 `Uvicorn running on http://0.0.0.0:8080` 표시
2. 브라우저에서 `http://localhost:8080` 접속 시 지도 UI 표시
3. 좌측 사이드바에 "시스템 상태: ✅ 정상" 표시
