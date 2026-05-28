# 텔레그램 급여 명세 발송 봇

구글 스프레드시트의 급여 데이터를 읽어 각자에게 1:1로 텔레그램 개별 발송하는 스크립트.
평소엔 꺼져 있고, 실행할 때만 동작합니다. (상시 서버 불필요)

- 직원: 2주 단위 / 슈퍼바이저: 월 단위 — 한 봇에서 프로필만 바꿔 발송
- 단체방 발송 금지, 각자 1:1 개별 발송 (민감정보 보호)

---

## 새로 설치하기 (다른 사람 컴퓨터에 본인 전용으로)

> 이 봇을 본인 것으로 새로 만드는 가이드입니다.
> **각자 별도의 봇 / 구글 계정 / 스프레드시트**를 사용하므로, 다른 사람과 키를 공유하지 않습니다.

### 0. 준비물
- 컴퓨터에 **Python 3.10 이상** 설치 (`python --version`으로 확인)
- 본인 **텔레그램** 계정
- 본인 **구글** 계정
- 급여 **스프레드시트** (구글 시트)

### 1. 코드 받기
```bash
git clone https://github.com/oneagency888-crypto/casino-schedule-miniapp.git
cd casino-schedule-miniapp/telegram-payroll-bot
```
(또는 GitHub에서 ZIP 다운로드 후 압축 해제)

### 2. 텔레그램 봇 만들기
1. 텔레그램에서 **@BotFather** 검색 → `/newbot`
2. 봇 이름 + 유저네임(`_bot`으로 끝나야 함) 입력
3. 받은 **토큰** 복사 (예: `7123456789:AAF...`)
4. 만든 봇을 검색해 본인이 먼저 `/start` 전송

### 3. Google 서비스 계정 만들기
1. [console.cloud.google.com](https://console.cloud.google.com) 접속
2. **새 프로젝트** 생성
3. **API 및 서비스 → 라이브러리** → `Google Sheets API`, `Google Drive API` 각각 **사용** 설정
4. **API 및 서비스 → 사용자 인증 정보** → **사용자 인증 정보 만들기 → 서비스 계정** (OAuth 아님!)
5. 만든 서비스 계정 → **키** 탭 → **키 추가 → 새 키 만들기 → JSON** → 파일 다운로드
6. 다운받은 파일을 `credentials/google-service-account.json` 위치에 저장

### 4. 스프레드시트 공유
1. JSON 파일 안의 `"client_email"` 값 복사 (`xxx@xxx.iam.gserviceaccount.com`)
2. 급여 스프레드시트 → **공유** → 이 이메일을 **뷰어**로 추가
3. 시트 URL에서 ID 확인: `docs.google.com/spreadsheets/d/`**여기가ID**`/edit`

### 5. 설정 파일 만들기 (.env)
`.env.example`을 복사해 `.env`로 만들고 값을 채웁니다.
```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```
`.env` 내용:
```
TELEGRAM_BOT_TOKEN=봇토큰
GOOGLE_CREDENTIALS_PATH=credentials/google-service-account.json
SPREADSHEET_ID=직원시트ID
SUPERVISOR_SPREADSHEET_ID=슈퍼바이저시트ID
SHEET_TAB_NAME=
TEST_CHAT_ID=본인chat_id
```
> 슈퍼바이저가 없으면 `SUPERVISOR_SPREADSHEET_ID`는 비워둬도 됩니다.

### 6. 가상환경 + 의존성 설치
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 7. chat_id 수집
1. 발송 대상자들에게 봇을 검색해 `/start`를 보내달라고 안내
2. 아래 실행 후 표시되는 chat_id를 스프레드시트에 입력
```bash
python scripts/get_chat_ids.py
```
- 직원 시트: **AH열**, 슈퍼바이저 시트: **AT열**에 각자 chat_id 입력
- 본인 chat_id는 `.env`의 `TEST_CHAT_ID`에도 넣기

### 8. 테스트 발송 (나에게만)
```bash
python scripts/send_payroll.py employee "5/11-5/24" --test
```
`--test`를 붙이면 모든 메시지가 `TEST_CHAT_ID`(나)에게만 갑니다. 형식 확인용.

### 9. 실제 발송
```bash
# 직원 (2주)
python scripts/send_payroll.py employee "5/11-5/24"
# 슈퍼바이저 (월)
python scripts/send_payroll.py supervisor "May"
```
- 마지막 인자는 **시트 탭 이름** (정확히 일치해야 함)
- AH/AT열에 chat_id가 있는 사람에게만 발송, 비어있으면 건너뜀

---

## 스프레드시트 컬럼이 다를 경우

이 코드의 컬럼 위치는 특정 시트 레이아웃 기준입니다. 새 사용자의 시트 구조가 다르면
`src/config.py`의 `PROFILES`에서 컬럼 인덱스(0-based, A=0, B=1 ...)와 항목을 맞춰주세요.

```python
"employee": {
    "name_col": 2,        # C열 = 이름
    "unit_col": 4,        # E열 = 숙소
    "hours_start": 6,     # G열부터
    "hours_end": 19,      # T열까지 일별 시간
    "usdt_col": 30,       # AE열 = 실수령액
    "chat_id_col": 33,    # AH열 = chat_id
    "items": [            # (라벨, 컬럼, 부호) 부호 +1 합산 / -1 차감
        ("팁", 23, 1),
        ("전기세 차감", 27, -1),
        ...
    ],
}
```

---

## 보안 주의
- `.env`, `credentials/`, `*.json`은 `.gitignore`에 포함되어 git에 올라가지 않습니다.
- 봇 토큰과 서비스 계정 키는 절대 코드/채팅/공개 저장소에 노출하지 마세요.
- 사람마다 별도 봇·키를 사용하고, 공유하지 마세요.
