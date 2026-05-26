import gspread
from google.oauth2.service_account import Credentials
from src.config import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID, SHEET_TAB_NAME, COL, DATA_START_ROW

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def _parse_number(value):
    if not value:
        return 0.0
    cleaned = str(value).replace(",", "").replace("$", "").replace("₱", "").replace("P", "").strip()
    if not cleaned or cleaned == "-":
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _get_cell(row, idx):
    if idx < len(row):
        return row[idx]
    return ""


def get_worksheet(tab_name=None):
    creds = Credentials.from_service_account_file(str(GOOGLE_CREDENTIALS_PATH), scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    name = tab_name or SHEET_TAB_NAME
    if name:
        return spreadsheet.worksheet(name)
    return spreadsheet.sheet1


def read_payroll_data(tab_name=None):
    ws = get_worksheet(tab_name)
    all_values = ws.get_all_values()
    period = ws.title

    employees = []
    for row_idx in range(DATA_START_ROW - 1, len(all_values)):
        row = all_values[row_idx]

        name = _get_cell(row, COL["name"]).strip()
        if not name:
            continue

        total_hours = 0.0
        for col_idx in range(COL["hours_start"], COL["hours_end"] + 1):
            total_hours += _parse_number(_get_cell(row, col_idx))

        usdt_total = _parse_number(_get_cell(row, COL["usdt_total"]))
        if usdt_total == 0.0:
            continue

        employees.append({
            "name": name,
            "nick_name": _get_cell(row, COL["nick_name"]).strip(),
            "unit": _get_cell(row, COL["unit"]).strip(),
            "shift": _get_cell(row, COL["shift"]).strip(),
            "total_hours": total_hours,
            "night_100": _parse_number(_get_cell(row, COL["night_100"])),
            "deduction_visa": _parse_number(_get_cell(row, COL["deduction_visa"])),
            "tip": _parse_number(_get_cell(row, COL["tip"])),
            "flight_ticket": _parse_number(_get_cell(row, COL["flight_ticket"])),
            "table_bonus": _parse_number(_get_cell(row, COL["table_bonus"])),
            "deduction_table": _parse_number(_get_cell(row, COL["deduction_table"])),
            "electric_deduction": _parse_number(_get_cell(row, COL["electric_deduction"])),
            "remarks": _parse_number(_get_cell(row, COL["remarks"])),
            "usdt_total": usdt_total,
            "allowance": _parse_number(_get_cell(row, COL["allowance"])),
            "chat_id": _get_cell(row, COL["chat_id"]).strip(),
        })

    return period, employees
