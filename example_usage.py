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
    write_file_with_header,
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


def example_with_user_request():
    """사용자 요청 사항 포함 로깅 예제"""
    print("\n=== 사용자 요청 사항 포함 로깅 예제 ===")

    # 사용자 요청 사항을 포함한 파일 생성
    log_file_create(
        "analysis.py",
        "데이터 분석 스크립트 생성",
        user_request="매출 데이터 분석을 위한 파이썬 스크립트를 만들어주세요"
    )

    # 사용자 요청 사항을 포함한 파일 수정
    log_file_modify(
        "config.json",
        "설정 파일 업데이트",
        user_request="데이터베이스 연결 정보를 설정 파일에 추가해주세요"
    )

    # 사용자 요청 사항을 포함한 커스텀 로깅
    log_custom(
        "FEATURE_ADD",
        "사용자 인증 기능 추가",
        {"module": "auth", "lines_added": 150},
        user_request="로그인/로그아웃 기능을 구현해주세요"
    )


def example_write_file_with_header():
    """파일 헤더와 함께 작성하는 예제"""
    print("\n=== 파일 헤더 작성 예제 ===")

    # Python 파일 작성
    python_code = '''def calculate_sum(a, b):
    """두 수의 합을 계산합니다"""
    return a + b

def calculate_average(numbers):
    """숫자 리스트의 평균을 계산합니다"""
    return sum(numbers) / len(numbers)
'''

    write_file_with_header(
        "calculator.py",
        python_code,
        user_request="간단한 계산기 함수를 만들어주세요 (합계, 평균)"
    )

    # JavaScript 파일 작성
    js_code = '''function greet(name) {
    return `Hello, ${name}!`;
}

function getCurrentTime() {
    return new Date().toLocaleString();
}
'''

    write_file_with_header(
        "utils.js",
        js_code,
        user_request="인사말과 현재 시간을 반환하는 함수를 만들어주세요"
    )


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
        # example_with_user_request()  # 사용자 요청 사항 포함 예제
        # example_write_file_with_header()  # 파일 헤더 작성 예제

        print("\n✅ 예제 실행 완료!")
        print("GitHub 저장소를 확인하여 커밋이 푸시되었는지 확인하세요.")
    else:
        print("\n예제 실행이 취소되었습니다.")
