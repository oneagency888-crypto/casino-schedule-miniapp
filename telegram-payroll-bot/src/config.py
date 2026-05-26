import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GOOGLE_CREDENTIALS_PATH = Path(os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials/google-service-account.json"))
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_TAB_NAME = os.environ.get("SHEET_TAB_NAME", "")
TEST_CHAT_ID = os.environ.get("TEST_CHAT_ID", "")

# 스프레드시트 컬럼 인덱스 (0-based)
COL = {
    "name": 2,              # C
    "nick_name": 3,         # D
    "unit": 4,              # E
    "shift": 5,             # F
    "hours_start": 6,       # G (일별 근무시간 시작)
    "hours_end": 19,        # T (일별 근무시간 끝)
    "night_100": 21,        # V - $100 Night
    "deduction_visa": 22,   # W - Deduction (-) 비자비용
    "tip": 23,              # X - Tip (+)
    "flight_ticket": 24,    # Y - Flight Ticket
    "table_bonus": 25,      # Z - Table Bonus
    "deduction_table": 26,  # AA - Deduction (테이블)
    "electric_deduction": 27,  # AB - Electric Deduction
    "remarks": 29,          # AD - Remarks (선불금/가불금)
    "usdt_total": 30,       # AE - USDT Total payment
    "allowance": 32,        # AG - Allowance (₱)
    "chat_id": 33,          # AH - chat_id
}

HEADER_ROW = 5
DATA_START_ROW = 6
