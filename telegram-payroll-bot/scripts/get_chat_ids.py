"""
직원들이 봇에게 /start를 보낸 뒤, 이 스크립트로 chat_id를 확인합니다.
표시된 chat_id를 스프레드시트 AH열에 입력하세요.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from src.config import TELEGRAM_BOT_TOKEN


def main():
    print("봇에게 /start를 보낸 사용자 목록을 조회합니다...\n")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("ok"):
        print(f"API 호출 실패: {data}")
        return

    results = data.get("result", [])
    if not results:
        print("아직 메시지가 없습니다.")
        print("직원들에게 봇을 검색해서 /start를 보내달라고 안내하세요.")
        return

    users = {}
    for update in results:
        msg = update.get("message", {})
        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        if chat_id and chat.get("type") == "private":
            users[chat_id] = {
                "chat_id": chat_id,
                "first_name": chat.get("first_name", ""),
                "last_name": chat.get("last_name", ""),
                "username": chat.get("username", ""),
            }

    if not users:
        print("개인 메시지가 없습니다.")
        return

    print(f"총 {len(users)}명이 봇에게 메시지를 보냈습니다:\n")
    print(f"{'chat_id':<15} {'이름':<20} {'username':<20}")
    print("-" * 55)
    for u in users.values():
        name = f"{u['first_name']} {u['last_name']}".strip()
        username = f"@{u['username']}" if u["username"] else "-"
        print(f"{u['chat_id']:<15} {name:<20} {username:<20}")

    print("\n위 chat_id를 스프레드시트 AH열에 해당 직원 행에 입력하세요.")


if __name__ == "__main__":
    main()
