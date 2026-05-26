import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GOOGLE_CREDENTIALS_PATH = Path(os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials/google-service-account.json"))
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_TAB_NAME = os.environ.get("SHEET_TAB_NAME", "")
TEST_CHAT_ID = os.environ.get("TEST_CHAT_ID", "")
