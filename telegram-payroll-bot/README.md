# 텔레그램 급여 명세 발송 봇

구글 스프레드시트의 급여 데이터를 읽어, 직원/슈퍼바이저 **각자에게 1:1로** 텔레그램 개별 발송하는 스크립트입니다.

- 평소엔 꺼져 있고, **실행할 때만** 동작합니다 (24시간 켜두는 서버 필요 없음).
- 직원은 **2주 단위**, 슈퍼바이저는 **월 단위** — 한 봇에서 발송 대상만 바꿔서 보냅니다.
- 단체방으로 보내지 않고 **각자 개인 채팅으로만** 보냅니다 (급여는 민감정보).

> 이 문서는 **컴퓨터를 처음 만지는 사람도** 따라 할 수 있도록 한 단계씩 설명합니다.
> 위에서 아래로 순서대로 진행하세요. 중간을 건너뛰면 안 됩니다.

---

# 1부. 처음 설치하기 (한 번만)

각 사용자는 **본인 전용** 봇 · 구글 계정 · 스프레드시트를 사용합니다.
다른 사람과 봇 토큰이나 키를 절대 공유하지 않습니다.

## 0단계. 준비물 확인

### 0-1. Python 3.10 이상 설치 확인
1. (Windows) 키보드 `윈도우키`를 누르고 `cmd` 입력 → **명령 프롬프트** 실행
2. 아래 명령을 입력하고 엔터:
   ```
   python --version
   ```
3. `Python 3.10.x` 이상이 나오면 OK.
   - `Python 3.9` 이하거나, `'python'은 내부 또는 외부 명령... 아닙니다` 오류가 나오면 설치 필요.

### 0-2. Python 설치 (이미 있으면 건너뛰기)
1. [python.org/downloads](https://www.python.org/downloads/) 접속 → **Download Python 3.x.x** 클릭
2. 설치 파일 실행 후 **맨 아래 "Add python.exe to PATH" 체크박스를 꼭 체크** (중요!)
3. **Install Now** 클릭 → 완료되면 명령 프롬프트를 새로 열고 0-1을 다시 확인

### 0-3. 그 밖에 필요한 것
- 본인 **텔레그램** 계정 (휴대폰 앱)
- 본인 **구글** 계정 (Gmail)
- 급여가 정리된 **구글 스프레드시트**

---

## 1단계. 코드 받기

두 방법 중 **하나만** 하면 됩니다.

### 방법 A. ZIP 다운로드 (git 모르면 이 방법)
1. GitHub 저장소 페이지 접속:
   `https://github.com/oneagency888-crypto/casino-schedule-miniapp`
2. 초록색 **`< > Code`** 버튼 → **Download ZIP**
3. 다운받은 ZIP을 원하는 폴더에 압축 해제 (예: `C:\payroll-bot`)
4. 명령 프롬프트에서 그 폴더 안의 `telegram-payroll-bot`으로 이동:
   ```
   cd C:\payroll-bot\casino-schedule-miniapp\telegram-payroll-bot
   ```

### 방법 B. git clone (git이 설치돼 있으면)
```
git clone https://github.com/oneagency888-crypto/casino-schedule-miniapp.git
cd casino-schedule-miniapp\telegram-payroll-bot
```

> **확인 포인트**: 명령 프롬프트 경로 끝이 `...\telegram-payroll-bot>` 으로 보이면 성공.
> 앞으로 모든 명령은 **이 폴더 안에서** 실행합니다.

---

## 2단계. 텔레그램 봇 만들기

1. 텔레그램 앱에서 상단 검색창에 **`BotFather`** 입력 → 파란 체크 표시(공식)가 있는 것 선택
2. 대화창 아래 **시작/START** 누르기
3. `/newbot` 입력하고 전송
4. BotFather가 봇 **이름**을 물어봄 → 아무 이름 입력 (예: `우리회사 급여봇`)
5. 봇 **유저네임**을 물어봄 → 반드시 **`bot`으로 끝나야 함** (예: `mycompany_payroll_bot`)
   - 이미 쓰는 이름이면 거절됨 → 다른 이름 시도
6. 성공하면 BotFather가 이런 메시지를 줍니다:
   ```
   Use this token to access the HTTP API:
   7123456789:AAF1x2y3z4abcd-EFGhijklmnop
   ```
   → 이 **토큰**을 메모장에 복사해 둡니다. (나중에 `.env`에 넣음)
7. 방금 만든 봇을 검색해서 들어간 뒤, **본인이 직접 `/start`를 보냅니다.**
   (이걸 안 하면 봇이 나에게 메시지를 못 보냅니다)

> **주의**: 토큰은 비밀번호입니다. 다른 사람에게 보여주거나 채팅에 올리지 마세요.

---

## 3단계. Google 서비스 계정 만들기 (가장 중요)

코드가 구글 시트를 자동으로 읽으려면, 구글이 발급하는 **"로봇 계정용 열쇠(JSON 키)"**가 필요합니다.

### 3-1. 프로젝트 만들기
1. [console.cloud.google.com](https://console.cloud.google.com) 접속 → 구글 로그인
2. 화면 상단 왼쪽 **프로젝트 선택** 드롭다운 클릭 → **새 프로젝트**
3. 프로젝트 이름 입력 (예: `payroll-bot`) → **만들기**
4. 생성 후 상단 드롭다운에서 방금 만든 프로젝트가 선택돼 있는지 확인

### 3-2. API 2개 켜기
1. 왼쪽 위 **☰ 메뉴** → **API 및 서비스** → **라이브러리**
2. 검색창에 `Google Sheets API` 입력 → 클릭 → **사용** 버튼 클릭
3. 다시 **라이브러리**로 가서 `Google Drive API` 검색 → 클릭 → **사용** 버튼 클릭

> 이 둘을 안 켜면 나중에 "API has not been used / disabled" 오류가 납니다.

### 3-3. 서비스 계정 만들기
1. **☰ 메뉴** → **API 및 서비스** → **사용자 인증 정보**
2. 상단 **+ 사용자 인증 정보 만들기** 클릭
3. 목록에서 **서비스 계정** 선택 (⚠️ "OAuth 클라이언트 ID" 아님!)
4. 서비스 계정 이름 입력 (예: `payroll-reader`) → **만들고 계속하기**
5. 역할(선택)·사용자(선택)는 그냥 **완료** 눌러 건너뜀

### 3-4. JSON 키 다운로드
1. 방금 만든 서비스 계정 이름을 클릭해 들어감
2. 위쪽 **키(Keys)** 탭 클릭
3. **키 추가** → **새 키 만들기** → 형식 **JSON** 선택 → **만들기**
4. `.json` 파일이 컴퓨터에 자동 다운로드됨 (예: `payroll-bot-abc123.json`)
5. 이 파일을 프로젝트 폴더 안 **`credentials`** 폴더에 넣고, 이름을
   **`google-service-account.json`** 으로 바꿉니다.
   - 최종 위치: `telegram-payroll-bot\credentials\google-service-account.json`
   - `credentials` 폴더가 없으면 직접 만드세요.

> **주의**: 이 JSON 파일도 비밀 키입니다. 절대 공유하거나 git에 올리지 마세요.

---

## 4단계. 스프레드시트를 서비스 계정에 공유

서비스 계정은 별도의 "로봇 구글 계정"이라, 시트를 **공유**해줘야 읽을 수 있습니다.

1. 위에서 받은 JSON 파일을 **메모장**으로 엽니다.
2. `"client_email"` 항목을 찾습니다:
   ```
   "client_email": "payroll-reader@payroll-bot.iam.gserviceaccount.com",
   ```
   → 이 이메일 주소를 복사합니다.
3. 급여 **스프레드시트**를 브라우저로 엽니다.
4. 우측 상단 **공유** 버튼 클릭 → 복사한 이메일 붙여넣기 → 권한 **뷰어** → **공유/보내기**
5. 스프레드시트 주소창에서 **시트 ID**를 확인해 메모해 둡니다:
   ```
   https://docs.google.com/spreadsheets/d/[이 부분이 시트 ID]/edit
   ```
   - 예: `1AbCdEfGhIjKlMnOpQrStUvWxYz1234567890`

> 슈퍼바이저용 시트가 따로 있으면, **그 시트도** 같은 이메일로 한 번 더 공유하고 ID를 따로 메모합니다.

---

## 5단계. 설정 파일(.env) 만들기

비밀 값들을 코드에 직접 쓰지 않고 `.env`라는 파일에 모아둡니다.

1. 명령 프롬프트(`telegram-payroll-bot` 폴더)에서:
   ```
   copy .env.example .env
   ```
   (Mac/Linux은 `cp .env.example .env`)
2. 메모장으로 `.env` 파일을 엽니다:
   ```
   notepad .env
   ```
3. 각 항목을 본인 값으로 채웁니다:
   ```
   TELEGRAM_BOT_TOKEN=7123456789:AAF1x2y3z4...     ← 2단계 토큰
   GOOGLE_CREDENTIALS_PATH=credentials/google-service-account.json   ← 그대로 둠
   SPREADSHEET_ID=1AbCdEf...                        ← 4단계 직원 시트 ID
   SUPERVISOR_SPREADSHEET_ID=1XyZ...                ← 슈퍼바이저 시트 ID (없으면 비움)
   SHEET_TAB_NAME=                                  ← 비워둠 (실행할 때 지정)
   TEST_CHAT_ID=                                    ← 7단계에서 채움
   ```
4. 저장하고 닫기 (`Ctrl+S`)

> `=` 양옆에 공백을 넣지 마세요. 따옴표도 붙이지 마세요.

---

## 6단계. 가상환경 만들고 프로그램 설치

가상환경(venv)은 이 프로젝트 전용 격리 공간입니다.

### Windows
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **확인 포인트**: 명령 프롬프트 줄 맨 앞에 `(.venv)`가 보이면 가상환경이 켜진 상태입니다.
>
> **Windows에서 `activate`가 빨간 오류**(execution policy)가 나면, **PowerShell을 관리자 권한으로** 열고
> 아래 한 줄을 실행한 뒤 다시 시도하세요:
> ```
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## 7단계. chat_id 수집

봇이 누구에게 보낼지 알려면, 각 사람의 고유 번호(chat_id)가 필요합니다.

1. 발송 대상자 전원에게 **봇을 검색해서 `/start`를 보내달라고** 안내합니다.
   (본인도 보내야 함 — 2단계에서 이미 했으면 OK)
2. 아래 명령 실행:
   ```
   python scripts/get_chat_ids.py
   ```
3. `/start`를 보낸 사람들의 chat_id가 표 형태로 나옵니다:
   ```
   chat_id          이름                  username
   -------------------------------------------------------
   7454418997       LOUIS J               @OneLouis8
   6983295492       AMY                   @amy_k
   ```
4. 이 chat_id를 스프레드시트의 chat_id 열에 **해당하는 사람 행**에 입력합니다.
   - 직원 시트: **AH열**
   - 슈퍼바이저 시트: **AT열**
5. **본인의 chat_id**는 `.env` 파일의 `TEST_CHAT_ID=` 뒤에도 넣고 저장합니다.

> **안 나올 때**: `/start`를 BotFather가 아니라 **내가 만든 봇**에게 보냈는지 확인하세요.
> 텔레그램은 최근 메시지만 보관하므로, 오래되면 다시 `/start`를 보내고 재실행하세요.

---

## 8단계. 테스트 발송 (나에게만)

실제 직원에게 보내기 전에, 형식이 맞는지 **나에게만** 먼저 보내봅니다.

```
python scripts/send_payroll.py employee "5/11-5/24" --test
```
- `employee` = 발송 대상 (직원). 슈퍼바이저는 `supervisor`
- `"5/11-5/24"` = **시트 탭 이름** (스프레드시트 아래 탭 이름과 정확히 같아야 함)
- `--test` = 모든 메시지를 나(`TEST_CHAT_ID`)에게만 보냄

→ 본인 텔레그램으로 급여 명세 메시지가 오면 성공입니다. 내용·형식을 확인하세요.

---

## 9단계. 실제 발송

테스트로 형식을 확인했으면, `--test`를 빼고 실제로 보냅니다.

```
# 직원 (2주 단위)
python scripts/send_payroll.py employee "5/11-5/24"

# 슈퍼바이저 (월 단위)
python scripts/send_payroll.py supervisor "May"
```
- chat_id가 입력된 사람에게만 발송되고, 비어있으면 자동으로 건너뜁니다.
- 실행 후 `OK / FAIL` 목록과 `성공 X명 / 실패 Y명` 요약이 나옵니다.

---

# 2부. 매번 발송할 때 (정기 사용법)

설치는 한 번만 하면 됩니다. 그 다음부터는 급여 정리가 끝날 때마다 아래만 반복하세요.

1. 스프레드시트에서 이번 기간 데이터가 다 채워졌는지 확인
2. 신규 입사자가 있으면 7단계로 chat_id 추가
3. 명령 프롬프트에서 `telegram-payroll-bot` 폴더로 이동
4. 가상환경 켜기:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
5. 테스트 발송으로 확인 → 실제 발송:
   ```
   python scripts/send_payroll.py employee "이번탭이름" --test
   python scripts/send_payroll.py employee "이번탭이름"
   ```

---

# 3부. 스프레드시트 컬럼이 다를 경우

이 코드의 컬럼 위치는 특정 시트 레이아웃 기준입니다. 새 사용자의 시트 구조가 다르면
`src/config.py`의 `PROFILES`에서 컬럼 번호를 그 시트에 맞게 바꿔야 합니다.

- 컬럼 번호는 **0부터** 셉니다: A=0, B=1, C=2, D=3, E=4, F=5, G=6 ...
- `items`의 부호: **+1은 더하는 항목**, **-1은 빼는(차감) 항목**

```python
"employee": {
    "name_col": 2,        # C열 = 이름
    "nick_name_col": 3,   # D열 = 닉네임
    "unit_col": 4,        # E열 = 숙소
    "shift_col": 5,       # F열 = 시프트
    "hours_start": 6,     # G열부터
    "hours_end": 19,      # T열까지 = 일별 근무시간
    "usdt_col": 30,       # AE열 = 실수령액(USDT)
    "allowance_col": 32,  # AG열 = 수당(₱), 없으면 None
    "chat_id_col": 33,    # AH열 = chat_id
    "items": [            # (라벨, 컬럼번호, 부호)
        ("팁", 23, 1),
        ("테이블보너스", 25, 1),
        ("전기세 차감", 27, -1),
        # ...
    ],
}
```

> 시트 구조가 헷갈리면, 컬럼 글자(A B C...)가 보이는 스크린샷을 준비해 도움을 요청하세요.

---

# 4부. 자주 나는 오류 (해결법)

| 증상 | 원인 / 해결 |
|------|-------------|
| `'python'은 ... 명령이 아닙니다` | Python 미설치 또는 PATH 미체크 → 0-2단계 재설치 (PATH 체크) |
| `activate` 실행 시 빨간 오류 | PowerShell에서 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError` | 가상환경 안 켰거나 설치 안 함 → 6단계 다시 |
| `KeyError: 'TELEGRAM_BOT_TOKEN'` | `.env` 파일이 없거나 값 누락 → 5단계 확인 |
| `PermissionError` / 시트 못 읽음 | 4단계 시트 공유 안 함, 또는 시트 ID 오타 |
| `API has not been used / disabled` | 3-2단계 Sheets/Drive API 안 켬 |
| `chat not found` / 발송 실패 | 그 사람이 봇에게 `/start`를 안 보냄, 또는 chat_id 오타 |
| `WorksheetNotFound` | 탭 이름 오타 → 스프레드시트 아래 탭 이름과 정확히 일치해야 함 |
| chat_id 목록이 비어있음 | 내 봇이 아닌 BotFather에 `/start` 보냄, 또는 메시지가 오래됨 |

---

# 5부. 보안 주의사항

- `.env`, `credentials/`, `*.json`은 `.gitignore`에 들어 있어 git에 올라가지 않습니다.
- **봇 토큰**과 **서비스 계정 JSON 키**는 비밀번호입니다. 채팅·이메일·공개 저장소에 올리지 마세요.
- 사람마다 **별도의 봇·키·시트**를 쓰고, 서로 공유하지 않습니다.
- 급여는 민감정보이므로 항상 1:1 개인 채팅으로만 발송합니다 (단체방 금지).
