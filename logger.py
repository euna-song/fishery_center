import os
import json
from datetime import datetime
from pathlib import Path
import subprocess

class ActionLogger:
    """모든 작업을 로깅하고 GitHub에 자동으로 커밋하는 시스템"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.repo_path, "action_logs.json")
        self.version_file = os.path.join(self.repo_path, "version.py")
        self._ensure_log_files()

    def _ensure_log_files(self):
        """로그 파일들이 존재하는지 확인하고 없으면 생성"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        if not os.path.exists(self.version_file):
            self._update_version_file([])

    def _update_version_file(self, logs):
        """version.py 파일 업데이트"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        version_count = len(logs) + 1

        content = f'''"""
Fishery Center - Version History
Last Updated: {timestamp}
Total Versions: {version_count}
"""

VERSION = "v{version_count}"
LAST_UPDATED = "{timestamp}"

# Change History
CHANGES = [
'''

        for i, log in enumerate(reversed(logs[-10:]), 1):  # 최근 10개만 표시
            content += f'''    {{
        "version": "v{len(logs) - i + 1}",
        "timestamp": "{log['timestamp']}",
        "action": "{log['action']}",
        "description": "{log['description']}"
    }},
'''

        content += ''']

def get_version():
    return VERSION

def get_last_updated():
    return LAST_UPDATED

def get_change_history():
    return CHANGES
'''

        with open(self.version_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def log_action(self, action_type, description, details=None, user_request=None):
        """작업 로깅

        Args:
            action_type: 작업 유형
            description: 작업 설명
            details: 상세 정보 딕셔너리
            user_request: 사용자 요청 사항
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = {
            "timestamp": timestamp,
            "action": action_type,
            "description": description,
            "user_request": user_request or "",
            "details": details or {}
        }

        # 로그 파일 읽기
        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)

        # 새 로그 추가
        logs.append(log_entry)

        # 로그 파일 쓰기
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        # version.py 업데이트
        self._update_version_file(logs)

        print(f"[LOG] {timestamp} - {action_type}: {description}")

        return log_entry

    def auto_commit_and_push(self, commit_message=None):
        """자동으로 변경사항을 커밋하고 푸시"""
        try:
            os.chdir(self.repo_path)

            # Git 상태 확인
            status = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True, check=True)

            if not status.stdout.strip():
                print("[INFO] 커밋할 변경사항이 없습니다.")
                return False

            # Git add
            subprocess.run(['git', 'add', '.'], check=True)

            # Commit message 생성
            if not commit_message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"Auto-commit: {timestamp}"

            # Git commit
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)

            # Git push
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)

            print(f"[SUCCESS] 변경사항이 GitHub에 푸시되었습니다: {commit_message}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Git 작업 실패: {e}")
            return False

    def log_and_commit(self, action_type, description, details=None, commit_message=None, user_request=None):
        """작업을 로깅하고 자동으로 커밋

        Args:
            action_type: 작업 유형
            description: 작업 설명
            details: 상세 정보 딕셔너리
            commit_message: 커밋 메시지
            user_request: 사용자 요청 사항
        """
        log_entry = self.log_action(action_type, description, details, user_request)

        if not commit_message:
            commit_message = f"{action_type}: {description}"

        self.auto_commit_and_push(commit_message)

        return log_entry


# 전역 logger 인스턴스
logger = ActionLogger()

# 편의 함수들
def log_file_create(filename, description="", user_request=None):
    """파일 생성 로깅

    Args:
        filename: 파일명
        description: 작업 설명
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(
        "FILE_CREATE",
        description or f"Created file: {filename}",
        {"filename": filename},
        user_request=user_request
    )

def log_file_modify(filename, description="", user_request=None):
    """파일 수정 로깅

    Args:
        filename: 파일명
        description: 작업 설명
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(
        "FILE_MODIFY",
        description or f"Modified file: {filename}",
        {"filename": filename},
        user_request=user_request
    )

def log_file_delete(filename, description="", user_request=None):
    """파일 삭제 로깅

    Args:
        filename: 파일명
        description: 작업 설명
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(
        "FILE_DELETE",
        description or f"Deleted file: {filename}",
        {"filename": filename},
        user_request=user_request
    )

def log_command(command, description="", user_request=None):
    """명령어 실행 로깅

    Args:
        command: 실행한 명령어
        description: 작업 설명
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(
        "COMMAND",
        description or f"Executed command: {command}",
        {"command": command},
        user_request=user_request
    )

def log_error(error_message, description="", user_request=None):
    """에러 로깅

    Args:
        error_message: 에러 메시지
        description: 작업 설명
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(
        "ERROR",
        description or f"Error occurred: {error_message}",
        {"error": error_message},
        user_request=user_request
    )

def log_custom(action_type, description, details=None, user_request=None):
    """커스텀 로깅

    Args:
        action_type: 작업 유형
        description: 작업 설명
        details: 상세 정보 딕셔너리
        user_request: 사용자 요청 사항
    """
    return logger.log_and_commit(action_type, description, details, user_request=user_request)


def write_file_with_header(filepath, content, user_request=None, author="euna-song"):
    """파일을 작성하고 상단에 헤더 주석 추가

    Args:
        filepath: 파일 경로
        content: 파일 내용
        user_request: 사용자 요청 사항
        author: 작성자명
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = os.path.basename(filepath)

    # 파일 확장자에 따라 주석 스타일 결정
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.py']:
        comment_start = '"""'
        comment_end = '"""'
        line_comment = '#'
    elif ext in ['.js', '.java', '.cpp', '.c', '.h']:
        comment_start = '/*'
        comment_end = '*/'
        line_comment = '//'
    elif ext in ['.html', '.xml']:
        comment_start = '<!--'
        comment_end = '-->'
        line_comment = '<!--'
    else:
        comment_start = '#'
        comment_end = '#'
        line_comment = '#'

    # 헤더 생성
    header = f'''{comment_start}
File: {filename}
Created: {timestamp}
Author: {author}
User Request: {user_request or "N/A"}
Description: {content.split(chr(10))[0] if content else ""}
{comment_end}

'''

    # 파일 작성
    full_content = header + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    # 로깅
    log_file_create(
        filename,
        f"Created file with header: {filename}",
        user_request=user_request
    )

    print(f"[SUCCESS] File created with header: {filepath}")
    return filepath


if __name__ == "__main__":
    # 테스트
    print("=== Logger System Test ===")
    log_custom("SYSTEM_INIT", "Logger system initialized", {"version": "1.0"})
