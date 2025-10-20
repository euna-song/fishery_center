"""
로거 시스템 테스트
사용자 요청 사항이 제대로 기록되는지 확인
"""

from logger import log_custom, write_file_with_header
import os

# 테스트 1: 사용자 요청 포함 로깅
print("테스트 1: 사용자 요청 사항 포함 로깅")
log_custom(
    "TEST",
    "사용자 요청 기능 테스트",
    {"test_id": 1},
    user_request=".py 파일 새로 저장할때 주석으로 내가 요청한 사항도 저장해줘. 로그파일에도 마찬가지고"
)

# 테스트 2: 파일 헤더 작성 테스트
print("\n테스트 2: 파일 헤더와 함께 작성")
test_code = '''def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
'''

write_file_with_header(
    os.path.join(os.path.dirname(__file__), "test_hello.py"),
    test_code,
    user_request="간단한 Hello World 프로그램을 만들어주세요"
)

print("\n✅ 테스트 완료! action_logs.json과 test_hello.py를 확인하세요.")
