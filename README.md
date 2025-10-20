# Fishery Center - 자동 로깅 & 버전 관리 시스템

모든 작업을 자동으로 로깅하고 GitHub에 커밋하는 시스템입니다.

## 🚀 기능

- ✅ 모든 작업 자동 로깅 (파일 생성/수정/삭제, 명령어 실행, 에러 등)
- ✅ 타임스탬프와 상세 정보 기록
- ✅ 자동 버전 관리 (version.py)
- ✅ 변경 이력 추적
- ✅ GitHub 자동 커밋 & 푸시
- ✅ 커스텀 로깅 지원

## 📁 파일 구조

```
fishery_center/
├── logger.py           # 핵심 로깅 시스템
├── example_usage.py    # 사용 예제
├── action_logs.json    # 로그 파일 (자동 생성)
├── version.py          # 버전 정보 (자동 생성)
└── README.md           # 문서
```

## 🔧 설치 및 설정

### 1. 저장소 클론
```bash
git clone git@github.com:euna-song/fishery_center.git
cd fishery_center
```

### 2. SSH 키 설정 (이미 완료)
- SSH 키가 GitHub에 등록되어 있어야 합니다.
- 테스트: `ssh -T git@github.com`

### 3. Git 사용자 정보 설정
```bash
git config user.name "euna-song"
git config user.email "euna960621@gmail.com"
```

## 📖 사용 방법

### 기본 사용법

```python
from logger import (
    log_file_create,
    log_file_modify,
    log_file_delete,
    log_command,
    log_error,
    log_custom
)

# 파일 생성 로깅
log_file_create("new_file.py", "새로운 파이썬 파일 생성")

# 파일 수정 로깅
log_file_modify("existing_file.py", "함수 추가")

# 파일 삭제 로깅
log_file_delete("old_file.py", "더 이상 사용하지 않는 파일 삭제")

# 명령어 실행 로깅
log_command("python train.py", "모델 학습 시작")

# 에러 로깅
log_error("ValueError: invalid input", "입력 검증 실패")
```

### 커스텀 로깅

```python
from logger import log_custom

# 데이터베이스 작업 로깅
log_custom(
    "DATABASE_QUERY",
    "사용자 데이터 조회",
    {
        "query": "SELECT * FROM users",
        "execution_time": "0.05s",
        "rows_affected": 10
    }
)

# API 호출 로깅
log_custom(
    "API_CALL",
    "외부 API 호출",
    {
        "endpoint": "/api/data",
        "method": "POST",
        "status_code": 200
    }
)
```

### 수동 커밋 (로깅만 하고 나중에 커밋)

```python
from logger import logger

# 로깅만 수행 (커밋 없음)
logger.log_action("TASK_START", "작업 시작", {"task_id": 1})
logger.log_action("TASK_PROGRESS", "작업 진행 중", {"progress": "50%"})
logger.log_action("TASK_COMPLETE", "작업 완료", {"task_id": 1})

# 나중에 수동으로 커밋
logger.auto_commit_and_push("작업 완료")
```

## 📊 로그 파일 형식

### action_logs.json
```json
[
  {
    "timestamp": "2025-10-20 21:05:30",
    "action": "FILE_CREATE",
    "description": "Created file: new_file.py",
    "details": {
      "filename": "new_file.py"
    }
  },
  {
    "timestamp": "2025-10-20 21:06:15",
    "action": "COMMAND",
    "description": "Executed command: python train.py",
    "details": {
      "command": "python train.py"
    }
  }
]
```

### version.py
```python
"""
Fishery Center - Version History
Last Updated: 2025-10-20 21:06:15
Total Versions: 42
"""

VERSION = "v42"
LAST_UPDATED = "2025-10-20 21:06:15"

CHANGES = [
    {
        "version": "v42",
        "timestamp": "2025-10-20 21:06:15",
        "action": "COMMAND",
        "description": "Executed command: python train.py"
    },
    # ... (최근 10개 변경사항)
]
```

## 🔍 지원하는 액션 타입

- `FILE_CREATE` - 파일 생성
- `FILE_MODIFY` - 파일 수정
- `FILE_DELETE` - 파일 삭제
- `COMMAND` - 명령어 실행
- `ERROR` - 에러 발생
- `DATABASE_QUERY` - 데이터베이스 쿼리
- `API_CALL` - API 호출
- `SYSTEM_INIT` - 시스템 초기화
- 기타 커스텀 액션 타입 자유롭게 추가 가능

## ⚙️ 작동 방식

1. **로깅**: 작업 정보를 `action_logs.json`에 저장
2. **버전 업데이트**: `version.py` 파일을 자동으로 업데이트
3. **Git 작업**:
   - `git add .` - 모든 변경사항 스테이징
   - `git commit -m "메시지"` - 커밋 생성
   - `git push origin main` - GitHub에 푸시

## 📝 예제 실행

```bash
python example_usage.py
```

⚠️ **주의**: 예제를 실행하면 실제로 GitHub에 커밋이 푸시됩니다!

## 🔐 보안

- SSH 키를 사용한 안전한 GitHub 연결
- 민감한 정보는 로그에 저장하지 않도록 주의
- `.gitignore`에 민감한 파일 추가 권장

## 🛠️ 트러블슈팅

### SSH 연결 실패
```bash
# SSH 키 테스트
ssh -T git@github.com

# known_hosts에 GitHub 추가
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### Push 실패
```bash
# Git 설정 확인
git config --list

# 원격 저장소 확인
git remote -v

# 브랜치 확인
git branch -a
```

## 📄 라이선스

MIT License

## 👤 작성자

euna-song (euna960621@gmail.com)

## 🔄 최신 업데이트

- 2025-10-20: 초기 버전 생성
  - 자동 로깅 시스템 구현
  - 버전 관리 시스템 구현
  - GitHub 자동 커밋/푸시 기능 구현