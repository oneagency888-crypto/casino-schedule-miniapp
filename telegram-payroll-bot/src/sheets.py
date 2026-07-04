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


def _find_col_by_headers(all_values, keywords, header_rows=(3, 4)):
    """Find column index by combined header text across header_rows. Case-insensitive exact match."""
    keyword_set = {k.strip().lower() for k in keywords}
    max_len = 0
    for r in header_rows:
        if r < len(all_values):
            max_len = max(max_len, len(all_values[r]))
    for col_idx in range(max_len):
        parts = []
        for row_idx in header_rows:
            if row_idx < len(all_values) and col_idx < len(all_values[row_idx]):
                cell = str(all_values[row_idx][col_idx]).strip()
                if cell:
                    parts.append(cell)
        combined = " ".join(parts).strip().lower()
        if combined in keyword_set:
            return col_idx
    return None


SUPERVISOR_ITEM_HEADERS = {
    "야간수당": ["$100 Night", "Night"],
    "보조금": ["Subsidy"],
    "항공권": ["Flight Ticket"],
    "공제": ["Deduction"],
    "전기세 차감": ["Electric Deduction"],
    "선불금 차감": ["Remarks"],
}


def _detect_supervisor_columns(all_values, profile):
    """Detect actual column positions from the sheet header. Adapts to month day-count differences."""
    p = dict(profile)
    p["items"] = list(profile["items"])

    def find(keywords, fallback):
        idx = _find_col_by_headers(all_values, keywords)
        return idx if idx is not None else fallback

    p["name_col"] = find(["Name", "Full Name"], p["name_col"])
    p["nick_name_col"] = find(["Nick Name", "Screen name"], p["nick_name_col"])
    p["unit_col"] = find(["Unit"], p["unit_col"])
    p["shift_col"] = find(["Shift"], p["shift_col"])
    p["chat_id_col"] = find(["chat_id", "id_chat"], p["chat_id_col"])
    p["usdt_col"] = find(["USDT Total payment", "Total payment", "USDT"], p["usdt_col"])

    working_col = _find_col_by_headers(all_values, ["WORKING"])
    if working_col is not None:
        p["hours_end"] = working_col - 1

    new_items = []
    for label, col, sign in p["items"]:
        keywords = SUPERVISOR_ITEM_HEADERS.get(label)
        if keywords:
            detected = _find_col_by_headers(all_values, keywords)
            if detected is not None:
                col = detected
        new_items.append((label, col, sign))
    p["items"] = new_items

    return p


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

    if profile == "supervisor":
        p = _detect_supervisor_columns(all_values, p)

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
