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

    def log_action(self, action_type, description, details=None):
        """작업 로깅"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = {
            "timestamp": timestamp,
            "action": action_type,
            "description": description,
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

    def log_and_commit(self, action_type, description, details=None, commit_message=None):
        """작업을 로깅하고 자동으로 커밋"""
        log_entry = self.log_action(action_type, description, details)

        if not commit_message:
            commit_message = f"{action_type}: {description}"

        self.auto_commit_and_push(commit_message)

        return log_entry


# 전역 logger 인스턴스
logger = ActionLogger()

# 편의 함수들
def log_file_create(filename, description=""):
    """파일 생성 로깅"""
    return logger.log_and_commit(
        "FILE_CREATE",
        description or f"Created file: {filename}",
        {"filename": filename}
    )

def log_file_modify(filename, description=""):
    """파일 수정 로깅"""
    return logger.log_and_commit(
        "FILE_MODIFY",
        description or f"Modified file: {filename}",
        {"filename": filename}
    )

def log_file_delete(filename, description=""):
    """파일 삭제 로깅"""
    return logger.log_and_commit(
        "FILE_DELETE",
        description or f"Deleted file: {filename}",
        {"filename": filename}
    )

def log_command(command, description=""):
    """명령어 실행 로깅"""
    return logger.log_and_commit(
        "COMMAND",
        description or f"Executed command: {command}",
        {"command": command}
    )

def log_error(error_message, description=""):
    """에러 로깅"""
    return logger.log_and_commit(
        "ERROR",
        description or f"Error occurred: {error_message}",
        {"error": error_message}
    )

def log_custom(action_type, description, details=None):
    """커스텀 로깅"""
    return logger.log_and_commit(action_type, description, details)


if __name__ == "__main__":
    # 테스트
    print("=== Logger System Test ===")
    log_custom("SYSTEM_INIT", "Logger system initialized", {"version": "1.0"})
