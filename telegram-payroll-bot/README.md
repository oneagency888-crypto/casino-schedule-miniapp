# 텔레그램 급여 명세 발송 봇

2주마다 구글 스프레드시트의 급여 데이터를 읽어 각 직원에게 1:1로 텔레그램 개별 발송하는 스크립트.

## 사전 준비

1. BotFather에서 텔레그램 봇 토큰 발급
2. Google Cloud 서비스 계정 키(JSON) 발급 → `credentials/google-service-account.json`
3. 스프레드시트를 서비스 계정 이메일에 공유
4. 각 직원이 봇에게 `/start` → `get_chat_ids.py`로 chat_id 수집 → 시트에 기록

## 설치 (Windows)

```bash
cd telegram-payroll-bot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 환경변수 설정

```bash
copy .env.example .env
# .env 파일을 열어 실제 값 입력
```

## 실행

```bash
# chat_id 수집 (최초 1회 + 신규 직원 추가 시)
python scripts/get_chat_ids.py

# 급여 발송
python scripts/send_payroll.py
```
