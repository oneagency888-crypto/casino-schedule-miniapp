"""
급여 명세 발송 메인 스크립트.

사용법:
  python scripts/send_payroll.py employee              # 직원 (탭은 SHEET_TAB_NAME)
  python scripts/send_payroll.py supervisor "May"      # 슈퍼바이저 + 탭 지정
  python scripts/send_payroll.py employee --test        # 나에게만 테스트 발송
  python scripts/send_payroll.py supervisor "May" --test
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import TEST_CHAT_ID, PROFILES
from src.sheets import read_payroll_data
from src.formatter import format_payroll_message
from src.telegram_sender import send_message


def main():
    test_mode = "--test" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    profile = args[0] if len(args) >= 1 else "employee"
    tab_name = args[1] if len(args) >= 2 else None

    if profile not in PROFILES:
        print(f"알 수 없는 프로필: {profile} (employee 또는 supervisor 중 하나)")
        return

    print(f"프로필: {profile}")
    print("스프레드시트에서 급여 데이터를 읽는 중...")
    period, employees = read_payroll_data(profile, tab_name)
    print(f"  기간: {period}")
    print(f"  직원 수: {len(employees)}명")

    sendable = [e for e in employees if e["chat_id"]]
    skipped = [e for e in employees if not e["chat_id"]]

    if skipped:
        print(f"\nchat_id 없어서 건너뛰는 인원 ({len(skipped)}명):")
        for e in skipped:
            print(f"  - {e['name']} ({e['nick_name']})")

    if not sendable:
        print("\n발송할 인원이 없습니다. chat_id를 확인하세요.")
        return

    if test_mode:
        if not TEST_CHAT_ID:
            print("\nTEST_CHAT_ID가 설정되지 않았습니다.")
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
