import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GOOGLE_CREDENTIALS_PATH = Path(os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials/google-service-account.json"))
SHEET_TAB_NAME = os.environ.get("SHEET_TAB_NAME", "")
TEST_CHAT_ID = os.environ.get("TEST_CHAT_ID", "")

EMPLOYEE_SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
SUPERVISOR_SPREADSHEET_ID = os.environ.get("SUPERVISOR_SPREADSHEET_ID", "")

HEADER_ROW = 5
DATA_START_ROW = 6

# 발송 프로필 (직원 2주 단위 / 슈퍼바이저 월 단위)
# items: (라벨, 컬럼 인덱스 0-based, 부호) — 부호 +1은 합산, -1은 차감
PROFILES = {
    "employee": {
        "spreadsheet_id": EMPLOYEE_SPREADSHEET_ID,
        "name_col": 2,         # C
        "nick_name_col": 3,    # D
        "unit_col": 4,         # E
        "shift_col": 5,        # F
        "hours_start": 6,      # G
        "hours_end": 19,       # T (14일)
        "usdt_col": 30,        # AE
        "allowance_col": 32,   # AG
        "chat_id_col": 33,     # AH
        "items": [
            ("야간수당", 21, 1),       # V
            ("팁", 23, 1),             # X
            ("테이블보너스", 25, 1),    # Z
            ("항공권", 24, 1),         # Y
            ("비자비용 차감", 22, -1),  # W
            ("테이블 차감", 26, -1),    # AA
            ("전기세 차감", 27, -1),    # AB
            ("선불금 차감", 29, -1),    # AD
        ],
    },
    "supervisor": {
        "spreadsheet_id": SUPERVISOR_SPREADSHEET_ID,
        "name_col": 2,         # C
        "nick_name_col": 3,    # D
        "unit_col": 4,         # E
        "shift_col": 5,        # F
        "hours_start": 6,      # G
        "hours_end": 36,       # AK (31일)
        "usdt_col": 44,        # AS
        "allowance_col": None,
        "chat_id_col": 45,     # AT
        "items": [
            ("야간수당", 38, 1),       # AM
            ("보조금", 40, 1),         # AO (Subsidy)
            ("항공권", 41, 1),         # AP
            ("공제", 39, -1),          # AN (Deduction)
            ("전기세 차감", 42, -1),    # AQ
            ("선불금 차감", 43, -1),    # AR (Remarks)
        ],
    },
}
