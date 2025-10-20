"""
로깅 시스템 사용 예제
이 파일은 logger.py를 사용하는 방법을 보여줍니다.
"""

from logger import (
    log_file_create,
    log_file_modify,
    log_file_delete,
    log_command,
    log_error,
    log_custom,
    logger
)

def example_basic_logging():
    """기본 로깅 예제"""
    print("\n=== 기본 로깅 예제 ===")

    # 파일 생성 로깅
    log_file_create("test_file.txt", "테스트 파일 생성")

    # 파일 수정 로깅
    log_file_modify("test_file.txt", "테스트 파일 내용 수정")

    # 명령어 실행 로깅
    log_command("python script.py", "스크립트 실행")

    # 에러 로깅
    log_error("FileNotFoundError: test.txt", "파일을 찾을 수 없음")


def example_custom_logging():
    """커스텀 로깅 예제"""
    print("\n=== 커스텀 로깅 예제 ===")

    # 데이터베이스 작업 로깅
    log_custom(
        "DATABASE_QUERY",
        "사용자 데이터 조회",
        {
            "query": "SELECT * FROM users WHERE id=1",
            "execution_time": "0.05s",
            "rows_affected": 1
        }
    )

    # API 호출 로깅
    log_custom(
        "API_CALL",
        "날씨 정보 조회",
        {
            "endpoint": "/api/weather",
            "method": "GET",
            "status_code": 200,
            "response_time": "0.3s"
        }
    )


def example_manual_commit():
    """수동 커밋 예제 (자동 커밋하지 않고 로깅만)"""
    print("\n=== 수동 커밋 예제 ===")

    # 로깅만 하고 커밋하지 않음
    logger.log_action("PROCESSING", "데이터 처리 시작", {"items": 100})
    logger.log_action("PROCESSING", "데이터 처리 진행 중", {"progress": "50%"})
    logger.log_action("PROCESSING", "데이터 처리 완료", {"items": 100, "success": True})

    # 모든 작업 완료 후 한 번에 커밋
    logger.auto_commit_and_push("데이터 처리 작업 완료")


def example_batch_operations():
    """배치 작업 로깅 예제"""
    print("\n=== 배치 작업 로깅 예제 ===")

    files = ["data1.csv", "data2.csv", "data3.csv"]

    for i, file in enumerate(files, 1):
        logger.log_action(
            "FILE_PROCESS",
            f"파일 처리 중 ({i}/{len(files)})",
            {"filename": file, "progress": f"{i}/{len(files)}"}
        )

    # 배치 작업 완료 후 커밋
    logger.auto_commit_and_push(f"배치 처리 완료: {len(files)}개 파일 처리")


if __name__ == "__main__":
    print("=" * 50)
    print("Logger System - 사용 예제")
    print("=" * 50)

    # 주의: 이 예제를 실행하면 실제로 GitHub에 커밋됩니다!
    print("\n⚠️  이 예제를 실행하면 실제로 로그가 기록되고 GitHub에 푸시됩니다.")
    response = input("계속하시겠습니까? (y/n): ")

    if response.lower() == 'y':
        # 시스템 초기화 로깅
        log_custom("SYSTEM_START", "로깅 시스템 예제 실행 시작", {"version": "1.0"})

        # 각 예제 실행 (원하는 예제의 주석을 해제하세요)
        # example_basic_logging()
        # example_custom_logging()
        # example_manual_commit()
        # example_batch_operations()

        print("\n✅ 예제 실행 완료!")
        print("GitHub 저장소를 확인하여 커밋이 푸시되었는지 확인하세요.")
    else:
        print("\n예제 실행이 취소되었습니다.")
