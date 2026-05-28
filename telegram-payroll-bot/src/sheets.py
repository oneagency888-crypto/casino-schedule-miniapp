import gspread
from google.oauth2.service_account import Credentials
from src.config import GOOGLE_CREDENTIALS_PATH, SHEET_TAB_NAME, PROFILES, DATA_START_ROW

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
    if idx is not None and idx < len(row):
        return row[idx]
    return ""


def get_worksheet(spreadsheet_id, tab_name=None):
    creds = Credentials.from_service_account_file(str(GOOGLE_CREDENTIALS_PATH), scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    name = tab_name or SHEET_TAB_NAME
    if name:
        return spreadsheet.worksheet(name)
    return spreadsheet.sheet1


def read_payroll_data(profile, tab_name=None):
    p = PROFILES[profile]
    if not p["spreadsheet_id"]:
        raise RuntimeError(f"'{profile}' 프로필의 스프레드시트 ID가 설정되지 않았습니다.")

    ws = get_worksheet(p["spreadsheet_id"], tab_name)
    all_values = ws.get_all_values()
    period = ws.title

    employees = []
    for row_idx in range(DATA_START_ROW - 1, len(all_values)):
        row = all_values[row_idx]

        name = _get_cell(row, p["name_col"]).strip()
        if not name:
            continue

        usdt_total = _parse_number(_get_cell(row, p["usdt_col"]))
        if usdt_total == 0.0:
            continue

        total_hours = 0.0
        for col_idx in range(p["hours_start"], p["hours_end"] + 1):
            total_hours += _parse_number(_get_cell(row, col_idx))

        items = []
        for label, col_idx, sign in p["items"]:
            amount = _parse_number(_get_cell(row, col_idx))
            if amount:
                items.append((label, sign * abs(amount)))

        allowance = 0.0
        if p["allowance_col"] is not None:
            allowance = _parse_number(_get_cell(row, p["allowance_col"]))

        employees.append({
            "name": name,
            "nick_name": _get_cell(row, p["nick_name_col"]).strip(),
            "unit": _get_cell(row, p["unit_col"]).strip(),
            "shift": _get_cell(row, p["shift_col"]).strip(),
            "total_hours": total_hours,
            "items": items,
            "usdt_total": usdt_total,
            "allowance": allowance,
            "chat_id": _get_cell(row, p["chat_id_col"]).strip(),
        })

    return period, employees
