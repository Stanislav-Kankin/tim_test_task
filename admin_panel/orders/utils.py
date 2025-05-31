import requests
from django.conf import settings


def send_broadcast_message(message):
    bot_token = settings.BOT_TOKEN
    base_url = f"https://api.telegram.org/bot{bot_token}"

    url = f"{base_url}/sendMessage"
    payload = {
        "chat_id": message.chat_id,  # Нужно заменить на id получателей (например, из базы пользователей)
        "text": message.text,
        "parse_mode": "HTML",
    }

    response = requests.post(url, data=payload)
    return response.ok
