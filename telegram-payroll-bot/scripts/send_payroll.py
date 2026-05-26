"""
급여 명세 발송 메인 스크립트.

사용법:
  python scripts/send_payroll.py                    # .env의 SHEET_TAB_NAME 탭 사용
  python scripts/send_payroll.py "5/11-5/24"        # 특정 탭 지정
  python scripts/send_payroll.py --test              # 나에게만 테스트 발송
  python scripts/send_payroll.py "5/11-5/24" --test  # 특정 탭 + 테스트
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import TEST_CHAT_ID
from src.sheets import read_payroll_data
from src.formatter import format_payroll_message
from src.telegram_sender import send_message


def main():
    test_mode = "--test" in sys.argv

    tab_name = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            tab_name = arg
            break

    print("스프레드시트에서 급여 데이터를 읽는 중...")
    period, employees = read_payroll_data(tab_name)
    print(f"  기간: {period}")
    print(f"  직원 수: {len(employees)}명")

    sendable = [e for e in employees if e["chat_id"]]
    skipped = [e for e in employees if not e["chat_id"]]

    if skipped:
        print(f"\nchat_id 없어서 건너뛰는 직원 ({len(skipped)}명):")
        for e in skipped:
            print(f"  - {e['name']} ({e['nick_name']})")

    if not sendable:
        print("\n발송할 직원이 없습니다. chat_id를 확인하세요.")
        return

    if test_mode:
        if not TEST_CHAT_ID:
            print("\nTEST_CHAT_ID가 .env에 설정되지 않았습니다.")
            return
        print(f"\n테스트 모드: 모든 메시지를 TEST_CHAT_ID ({TEST_CHAT_ID})로 발송합니다.")

    print(f"\n{len(sendable)}명에게 발송 시작...\n")

    success = 0
    failed = 0

    for e in sendable:
        msg = format_payroll_message(e, period)
        target_id = TEST_CHAT_ID if test_mode else e["chat_id"]

        try:
            send_message(target_id, msg)
            print(f"  OK  {e['name']} ({e['nick_name']})")
            success += 1
        except Exception as err:
            print(f"  FAIL  {e['name']} ({e['nick_name']}) - {err}")
            failed += 1

        time.sleep(0.5)

    print(f"\n{'=' * 30}")
    print(f"발송 완료: {success}명 성공 / {failed}명 실패")


if __name__ == "__main__":
    main()
